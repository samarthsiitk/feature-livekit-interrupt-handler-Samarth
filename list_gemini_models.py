import google.generativeai as genai

genai.configure(api_key="AIzaSyCvL9_j3dkYzCk-adDa3pWuXKKOxMc5Ckw")
for model in genai.list_models():
    print(model.name, model.supported_generation_methods)
