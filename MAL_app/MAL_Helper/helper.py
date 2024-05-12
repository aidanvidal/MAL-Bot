import json
import time
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
import os
from .main import get_anime_list, get_anime_details, get_anime_rankings, get_suggestions, get_seasonal_anime, update_anime_status
load_dotenv()
client = OpenAI(
    api_key=os.getenv('OPENAI')
)
assistant = client.beta.assistants.update(
  "asst_Xg27YAJvGPrDmkn6DlvvedwY",
  instructions="You are a bot that helps with getting information about anime from myanimelist.net.",
  name="MyAnimeList Bot",
  tools=json.load(open('MAL_app/MAL_Helper/functions.json')),
  model="gpt-3.5-turbo",
)



def process_message(content, token=None):
    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=content
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    while run.status == "in_progress" or run.status == "queued":
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

        if run.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            response = messages.data[0].content[0].text.value
            return response

        if run.status == 'requires_action':
            # Get function name
            func = run.required_action.submit_tool_outputs.tool_calls[0].function.name
            # Get anime list
            if func == 'get_anime_list':
                # Get parameters
                username = json.loads(run.required_action.submit_tool_outputs.tool_calls[0].function.arguments).get('user_name', '@me')
                limit = json.loads(run.required_action.submit_tool_outputs.tool_calls[0].function.arguments).get('limit', 5)
                sort = json.loads(run.required_action.submit_tool_outputs.tool_calls[0].function.arguments).get('sort', 'list_score')
                status = json.loads(run.required_action.submit_tool_outputs.tool_calls[0].function.arguments).get('status', 'completed')
                offset = json.loads(run.required_action.submit_tool_outputs.tool_calls[0].function.arguments).get('offset', 0)
                # Get output
                if token is None and username == '@me':
                    output = "Please log in to get your anime list."
                elif token is None:
                    output = get_anime_list(username, limit, sort, status, offset)
                else:
                    output = get_anime_list(username, limit, sort, status, offset, token)
                print('used get_anime_list')
                run = client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=[{
                        "tool_call_id": run.required_action.submit_tool_outputs.tool_calls[0].id,
                        "output": output
                    }]
                )
            # Get anime details
            if func == 'get_anime_details':
                # Get parameters
                anime_title = json.loads(run.required_action.submit_tool_outputs.tool_calls[0].function.arguments).get('anime_title')
                # Get output
                if token is None:
                    output = get_anime_details(anime_title)
                else:
                    output = get_anime_details(anime_title, token)
                print('used get_anime_details')
                run = client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=[{
                        "tool_call_id": run.required_action.submit_tool_outputs.tool_calls[0].id,
                        "output": output
                    }]
                )
            # Get anime rankings
            if func == 'get_anime_rankings':
                # Get parameters
                limit = json.loads(run.required_action.submit_tool_outputs.tool_calls[0].function.arguments).get('limit', 5)
                ranking_type = json.loads(run.required_action.submit_tool_outputs.tool_calls[0].function.arguments).get('ranking_type', 'all')
                offset = json.loads(run.required_action.submit_tool_outputs.tool_calls[0].function.arguments).get('offset', 0)
                # Get output
                if token is None:
                    output = get_anime_rankings(limit, ranking_type, offset)
                else:
                    output = get_anime_rankings(limit, ranking_type, offset, token)
                print('used get_anime_rankings')
                run = client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=[{
                        "tool_call_id": run.required_action.submit_tool_outputs.tool_calls[0].id,
                        "output": output
                    }]
                )
            # Get anime recommendations
            if func == 'get_suggestions':
                # Get parameters
                limit = json.loads(run.required_action.submit_tool_outputs.tool_calls[0].function.arguments).get('limit', 5)
                offset = json.loads(run.required_action.submit_tool_outputs.tool_calls[0].function.arguments).get('offset', 0)
                # Get output
                if token is None:
                    output = "Please log in to get anime suggestions."
                else:
                    output = get_suggestions(limit, offset, token)
                print('used get_suggestions')
                run = client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=[{
                        "tool_call_id": run.required_action.submit_tool_outputs.tool_calls[0].id,
                        "output": output
                    }]
                )
            # Get seasonal anime list
            if func == 'get_seasonal_anime':
                # Get parameters
                year = json.loads(run.required_action.submit_tool_outputs.tool_calls[0].function.arguments).get('year', datetime.now().year)
                # Get current season
                current_season = datetime.now().month
                temp = ''
                if 1 <= current_season <= 3:
                    temp = 'winter'
                elif 4 <= current_season <= 6:
                    temp = 'spring'
                elif 7 <= current_season <= 9:
                    temp = 'summer'
                else:
                    temp = 'fall'
                season = json.loads(run.required_action.submit_tool_outputs.tool_calls[0].function.arguments).get('season', temp)
                limit = json.loads(run.required_action.submit_tool_outputs.tool_calls[0].function.arguments).get('limit', 5)
                offset = json.loads(run.required_action.submit_tool_outputs.tool_calls[0].function.arguments).get('offset', 0)
                # Get output
                if token is None:
                    output = get_seasonal_anime(year, season, limit, offset)
                else:
                    output = get_seasonal_anime(year, season, limit, offset, token)
                print('used get_seasonal_anime')
                run = client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=[{
                        "tool_call_id": run.required_action.submit_tool_outputs.tool_calls[0].id,
                        "output": output
                    }]
                )
            # Update anime status
            if func == 'update_anime_status':
                # Get parameters
                anime_title = json.loads(run.required_action.submit_tool_outputs.tool_calls[0].function.arguments).get('anime_title')
                status = json.loads(run.required_action.submit_tool_outputs.tool_calls[0].function.arguments).get('status')
                score = json.loads(run.required_action.submit_tool_outputs.tool_calls[0].function.arguments).get('score')
                is_rewatching = json.loads(run.required_action.submit_tool_outputs.tool_calls[0].function.arguments).get('is_rewatching')
                # Get output
                if token is None:
                    output = "Please log in to update anime status."
                else:
                    output = update_anime_status(anime_title, status, score, is_rewatching, token)
                print('used update_anime_status')
                run = client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=[{
                        "tool_call_id": run.required_action.submit_tool_outputs.tool_calls[0].id,
                        "output": output
                    }]
                )
    return None