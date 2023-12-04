from data import disorders2
symptoms = ["symptom 3"]
for disorder, stages in disorders2.items():
     # print(stages)
    for stage, symp in stages.items():
           if any(symptom in symp for symptom in symptoms):
                print(f"""
Disorder: {disorder}
Stage: {stage}
Detected Symptoms: {', '.join(symp)}
""")