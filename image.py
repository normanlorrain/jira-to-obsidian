import re



def removeSpaces(lines:str):
    fixed =  re.sub(r'image \(', r'image(', lines, flags=re.MULTILINE)
    return fixed


# def fixImages(lines:str):
#     fixed =  re.sub(r'\!(image.*?)\|thumbnail\!', r'![image](\1)', lines)
#     return fixed


# if __name__ == "__main__":
#     teststring="!image (565ac4a0-4f4b-4e87-b730-0f10361aa2f7).png|thumbnail!"

#     print(fixImages(teststring))


#     teststring="""## Comments
# ### 2022-06-13T11:14:13.032-0600

# !image (565ac4a0-4f4b-4e87-b730-0f10361aa2f7).png|thumbnail!
# !image (79f24901-90b4-4712-9717-729083f7bbe8).png|thumbnail!


# !image (f9978d4a-9c5c-4bd2-bccf-1dcf33d0f58e).png|thumbnail!
# !image (fa2ea9f7-b527-4706-9d6d-a804b732a0d0).png|thumbnail!"""

#     print(fixImages(teststring))
