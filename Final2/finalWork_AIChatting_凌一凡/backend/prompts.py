import os

prompt_short = """请将回复控制在500字以内"""
summary_prompt = """
        请为以下对话生成简洁摘要，保留关键信息和上下文:

        {}

        摘要应包含:
        1. 对话主题和关键信息
        2. 已达成的共识或结论   
        3. 待解决的问题(如有)
        4. 用户的偏好和特点(如有)
        
        摘要:
    """
# 角色相关
prompts = {
    'short':prompt_short,
    'character':{
        'englishTacher': open('./backend/prompts/englishTeacher.md').read(),
        'fitnessCoach': open('./backend/prompts/fitnessCoach.md').read(),
    }
}


if __name__ == '__main__':
    print(prompts['character']['fitnessCoach'])