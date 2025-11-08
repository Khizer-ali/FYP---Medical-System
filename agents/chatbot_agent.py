"""
Chatbot Agent - Medical chatbot that uses patient context for responses
"""
try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("Warning: transformers library not available. Using fallback responses.")

class ChatbotAgent:
    """Agent responsible for medical chatbot functionality"""
    
    def __init__(self):
        # Model can be easily changed by modifying this variable
        # Popular options: "microsoft/DialoGPT-medium", "facebook/blenderbot-400M-distill"
        self.model_name = "microsoft/DialoGPT-medium"
        self.chatbot = None
        if TRANSFORMERS_AVAILABLE:
            self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the chatbot model from Hugging Face"""
        try:
            # Using text-generation pipeline - simple and reliable
            # Model will be downloaded from Hugging Face on first use
            self.chatbot = pipeline(
                "text-generation",
                model=self.model_name,
                tokenizer=self.model_name,
                max_length=512,
                do_sample=True,
                temperature=0.7,
                device=-1  # Use CPU by default (-1), change to 0 for GPU if available
            )
            print(f"Successfully loaded model: {self.model_name}")
        except Exception as e:
            print(f"Warning: Could not load model {self.model_name}: {str(e)}")
            print("Using fallback response system (still functional)")
            self.chatbot = None
    
    def build_context(self, patient_context):
        """Build context string from patient data"""
        context_parts = []
        
        if patient_context.get('patient'):
            patient = patient_context['patient']
            context_parts.append(f"Patient: {patient.get('name')} (Ref: {patient.get('reference_number')})")
        
        # Add documents context
        if patient_context.get('documents'):
            context_parts.append("\nMedical Documents:")
            for doc in patient_context['documents']:
                if doc.get('parsed_text'):
                    # Use first 500 chars of each document
                    text = doc['parsed_text'][:500]
                    context_parts.append(f"- {doc.get('document_type', 'Document')}: {text}...")
        
        # Add vitals context
        if patient_context.get('vitals'):
            latest_vitals = patient_context['vitals'][-1]  # Most recent
            context_parts.append("\nLatest Vital Signs:")
            if latest_vitals.get('temperature'):
                context_parts.append(f"Temperature: {latest_vitals['temperature']}°C")
            if latest_vitals.get('weight'):
                context_parts.append(f"Weight: {latest_vitals['weight']} kg")
            if latest_vitals.get('height'):
                context_parts.append(f"Height: {latest_vitals['height']} cm")
            if latest_vitals.get('blood_pressure_systolic'):
                context_parts.append(f"Blood Pressure: {latest_vitals['blood_pressure_systolic']}/{latest_vitals.get('blood_pressure_diastolic', '')} mmHg")
            if latest_vitals.get('heart_rate'):
                context_parts.append(f"Heart Rate: {latest_vitals['heart_rate']} bpm")
        
        # Add family history context
        if patient_context.get('family_history'):
            context_parts.append("\nFamily History:")
            for fh in patient_context['family_history']:
                context_parts.append(f"- {fh.get('condition')} ({fh.get('relation', 'Unknown relation')})")
        
        return "\n".join(context_parts)
    
    def generate_response(self, question, patient_context):
        """Generate response to user question using patient context"""
        # Build context
        context = self.build_context(patient_context)
        
        # Create prompt
        prompt = f"""Medical Context:
{context}

Question: {question}

Answer:"""
        
        if self.chatbot:
            try:
                # Generate response using the model
                response = self.chatbot(
                    prompt,
                    max_new_tokens=200,
                    num_return_sequences=1,
                    pad_token_id=self.chatbot.tokenizer.eos_token_id if hasattr(self.chatbot.tokenizer, 'eos_token_id') else None,
                    truncation=True
                )
                
                if isinstance(response, list) and len(response) > 0:
                    generated_text = response[0].get('generated_text', '')
                    # Extract just the answer part (remove the prompt)
                    if 'Answer:' in generated_text:
                        answer = generated_text.split('Answer:')[-1].strip()
                    elif prompt in generated_text:
                        answer = generated_text.replace(prompt, '').strip()
                    else:
                        answer = generated_text.strip()
                    
                    # Clean up the answer
                    if answer:
                        return answer[:500]  # Limit response length
            except Exception as e:
                print(f"Error generating response: {str(e)}")
        
        # Fallback response if model not available
        return self._fallback_response(question, context)
    
    def _fallback_response(self, question, context):
        """Fallback response system when model is not available"""
        question_lower = question.lower()
        
        # Simple keyword-based responses
        if any(word in question_lower for word in ['temperature', 'fever', 'temp']):
            return "Based on the patient's vital signs, I can see their temperature readings. Please review the latest vitals for current temperature status."
        
        if any(word in question_lower for word in ['weight', 'bmi', 'body mass']):
            return "The patient's weight and height measurements are available in their vital signs. You can calculate BMI using weight (kg) / height (m)²."
        
        if any(word in question_lower for word in ['blood pressure', 'bp', 'hypertension']):
            return "Blood pressure readings are recorded in the patient's vital signs. Please check the latest measurements for current status."
        
        if any(word in question_lower for word in ['family history', 'genetic', 'hereditary']):
            return "Family history information is available in the patient's records. Please review the family history section for details."
        
        if any(word in question_lower for word in ['document', 'report', 'test result']):
            return "Medical documents and reports have been uploaded and parsed. Please review the documents section for detailed information."
        
        return f"I have access to the patient's medical records including documents, vital signs, and family history. Based on the context: {context[:200]}... How can I help you with this patient's care?"

