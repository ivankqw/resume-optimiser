import dash
import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash import Input, Output, State
import base64
import docx
import io
from resume_parse import *
from gpt3_wrapper import *

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
app.layout = html.Div(children=[
    html.H1('Resume Optimiser', style={'textAlign':'center'}),
    html.H4('Powered by GPT-3', style={'textAlign':'center'}),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div(children = [
                        dcc.Upload(id = "file_upload", children = html.Div(['Drag and Drop or ',
            html.A('Select Files')])),
                     dbc.Input(id="job-description", placeholder="Copy Job Description Here", type="text")
                    ])),
                    dbc.Col(html.Div(children = [dbc.Input(id="output_area", placeholder="New Resume", type="text")]))
                ]
            )
        ]
    )


])
def parse_contents(contents, filename, jd):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    if 'docx' in filename:
        # read docx
        doc = docx.Document(io.BytesIO(decoded))
        parsed_resume = '\n\n'.join([paragraph.text for paragraph in doc.paragraphs])
        # extract experiences and skills
        experience = extract_experiences(parsed_resume)
        skills = extract_skills(parsed_resume)
        print("OLD EXPERIENCE: ", experience)
        print("OLD SKILLS: ", skills)
        # use gpt-3 to extract keywords from jd 
        keywords = get_keywords(jd)
        # use keywords to rewrite resume
        result = rewrite_resume({
            experience: experience,
            skills: skills
        }, keywords)
        print(result)
        return "OLD EXPERIENCE: " + experience + "\n\n" + "OLD SKILLS: " + skills + "NEW EXPERIENCE: " + result.get('experience') + "\n\n" + "NEW SKILLS: " + result.get('skills')  
    else:
        return 'Invalid file type'

@app.callback(
    Output('output_area','value'), 
    Input('file_upload', 'contents'),
    Input('file_upload', 'filename'),
    Input('job-description','value')
    )

def update_output(contents, filename, jd):
    if contents is not None:
        return parse_contents(contents, filename, jd)
    print(jd)


if __name__ == "__main__":
    app.run_server(debug=True)
