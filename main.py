import openai
from fastapi import FastAPI, Form, Request
from typing import Annotated
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)

templates = Jinja2Templates(directory="templates")

chat_responses = []


@app.get("/", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "chat_responses": chat_responses})

chat_log = [{
        'role': 'system',
        'content': "You are Vishvam's personal chatbot. Vishvam studies Computer Engineering at the University of Waterloo."
    },
    {
        'role': 'system',
        'content': "Experience: \n"
                    "Software Engineering Intern Sept - Dec 2023\nAvolta Inc Toronto, Ontario\n• Developed a POST API using Flask and Python for user registration, ensuring data validation and uniqueness.\n• Built a Flask API endpoint capable of processing GET and POST requests, aiding in mobile app testing and debugging.\n• Utilized SQL tools to design an efficient database for vehicle data including brand-specific tables for data retrieval.\n• Created a function using Python’s CSV module to automate the import of vehicle data from CSVs to their SQL tables.\n\n"
                    "Business Analyst Sept - Dec 2023\nSungrid Solutions Cambridge, Ontario\n• Utilized Smartsheet for data collection , enabling data-driven decision making and cost optimization.\n• Developed an organization chart web app using d3.js, python, and Smartsheet API for data visualization.\n• Conducted negotiations with vendors for inventory procurement ensuring cost-effective sourcing.\n• Managed all IT-related issues in the company in order to improve system efficiency and led the team effectively.\n\n"
                    "Cloud Developer Jan - Apr 2023\nISED Canada Ottawa, Ontario\n• Automated EC2 instance scheduling using AWS CloudFormation and CDK, decreasing resource costs by 50%.\n• Used Python and Boto3 to setup AWS Lambda for CloudWatch Alarms, reducing setup time across 50+ EC2 instances.\n• Optimized EC2 instances using monitoring techniques to boost application responsiveness and minimize latency.\n• Implemented EC2 auto-scaling groups using Python and SDK, ensuring high availability and system reliability."
    },
    {
        'role': 'system',
        'content': "Favourite singer or songs Vishvam Likes. Vishvam's favourite singer is Arijit Singh. His song Tum hi Ho is the best and many other hits like Apna Bana Le etc. Vishvam's current favourite song is Ve Kameleya."
    }
    ]


@app.post("/", response_class=HTMLResponse)
async def chat(request: Request, user_input: Annotated[str, Form()]):

    chat_log.append({'role': 'user', 'content': user_input})
    chat_responses.append(user_input)

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=chat_log,
        temperature=0.6
    )

    bot_response = response['choices'][0]['message']['content']
    chat_log.append({'role': 'assistant', 'content': bot_response})
    chat_responses.append(bot_response)

    return templates.TemplateResponse("home.html", {"request": request, "chat_responses": chat_responses})


@app.get("/image", response_class=HTMLResponse)
async def image_page(request: Request):
    return templates.TemplateResponse("image.html", {"request": request})


@app.post("/image", response_class=HTMLResponse)
async def create_image(request: Request, user_input: Annotated[str, Form()]):

    response = openai.Image.create(
        prompt=user_input,
        n=1,
        size="512x512"
    )

    image_url = response['data'][0]['url']
    return templates.TemplateResponse("image.html", {"request": request, "image_url": image_url})

@app.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})