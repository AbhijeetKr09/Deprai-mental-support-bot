from data import disorders

class DisorderPredictor:
    
    def __init__(self):
        self.disorders = disorders

    def predict(self, symptoms):

        for disorder, stages in self.disorders.items():
            for stage, symptom in stages.items():
                if symptoms.issubset(symptom):
                    return (disorder, stage, symptoms)

        return "No Disorder Detected"       


if __name__ == "__main__":

    pred = DisorderPredictor()
    disorder, stage, symptoms = pred.predict({"Symptom 4"})

    print(f"""
Disorder: {disorder}
stage: {stage}
Symptoms: {", ".join(symptoms)}
""")


