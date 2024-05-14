from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from key.env
load_dotenv('key.env')

client = OpenAI()

# completion = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
#         {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
#     ]
# )
#
# print(completion.choices[0].message)


# response = client.images.generate(
#     model="dall-e-3",
#     prompt="a white siamese cat",
#     size="1024x1024",
#     quality="standard",
#     n=1,
# )
#
# image_url = response.data[0].url
# print(image_url)



# response = client.chat.completions.create(
#     model="gpt-4-vision-preview",
#     messages=[
#         {
#             "role": "user",
#             "content": [
#                 {"type": "text", "text": "Look at this image and write an essay on what comes to your mind after seeing it"},
#                 {
#                     "type": "image_url",
#                     "image_url": {
#                         "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
#                     },
#                 },
#             ],
#         }
#     ],
#     max_tokens=1000,
# )
#
# print(response.choices[0])


speech_file_path = Path(__file__).parent / "speech.mp3"
print(speech_file_path)
response = client.audio.speech.create(
    model="tts-1",
    voice="onyx",
    input="You speak harshly, but truly. Your words cut deeper than any sword"
)

response.stream_to_file(speech_file_path)