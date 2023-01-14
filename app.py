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
    html.H4('Powered by ChatGPT', style={'textAlign':'center'}),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div(children = [
                        dcc.Upload(id = "file_upload", children = html.Div(['Drag and Drop or ',
            html.A('Select Files')])),
                        html.Div(id="file-name",children="No File Uploaded"),
                        html.Br(),
                     dbc.Textarea(id="job-description", placeholder="Copy Job Description Here")
                    ])),
                    dbc.Col(id = "boost", children=[dbc.Label("Bullshit Meter", html_for="slider"),
                    dcc.Slider(id="bullshit", min=0, max=10, step=1, value=3),
                    dbc.Button("Boost Resume",color="primary",id="boost-btn",n_clicks=0)
                    ]),
                    dbc.Col(html.Div(children = [dbc.Textarea(id="output_area", placeholder="New Resume")]))
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
        resume_dict = {}
        resume_dict['experience'] = experience
        resume_dict['skills'] = skills
        # use gpt-3 to extract keywords from jd 
        keywords = get_keywords(jd)
        # use keywords to rewrite resume
        result = rewrite_resume(resume_dict, keywords)
        print(result)
        return "OLD EXPERIENCE: " + experience + "NEW EXPERIENCE: " + result.get('experience') + "\n\n" + "OLD SKILLS: " + skills +  "\n\n" + "NEW SKILLS: " + result.get('skills')  
    else:
        return 'Invalid file type'

@app.callback(
    Output("file-name", 'children'),
    Input('file_upload', 'filename')
)

def show_upload_name(filename):
    if filename:
        return filename
    else:
        return "No File Uploaded"

@app.callback(
    Output('output_area','value'),
    Input('boost-btn','n_clicks'), 
    State('file_upload', 'contents'),
    State('file_upload', 'filename'),
    State('job-description','value'),
    State('bullshit','value')
    )
def update_output(n_clicks,contents, filename, jd, bullshit):
    if contents is not None:
        return parse_contents(contents, filename, jd)
    print(jd)


if __name__ == "__main__":
    app.run_server(debug=True)
