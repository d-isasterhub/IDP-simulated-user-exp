from v2_interview import read_human_data, create_userprofiles


data = read_human_data("user-study/data-exploration-cleanup/cleaned_simulatedusers.csv")
profiles = create_userprofiles(data)

for p in profiles:
    print(p)
