    response = client.chat.completions.create(>
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Eres un analista legal experto en procesos judiciales colombianos."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return {"resultado": response.choices[0].message.content}
