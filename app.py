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

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
app.layout = html.Div(children=[
    html.H1('Test Dash App', style={'textAlign':'center'}),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div(children = [
                        dcc.Upload(id = "file_upload", children = html.Div(['Drag and Drop or ',
            html.A('Select Files')])),
                    dcc.Textarea(
        id='textarea-example',
        value='Copy Job Description Here',
        style={'width': '100%', 'height': 300},
    )
                    ])),
                    dbc.Col(html.Div(children = [dcc.Textarea(
        id='output_area',
        value='Output',
        style={'width': '100%', 'height': 300},
    )]))
                ]
            )
        ]
    )


])
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    if 'docx' in filename:
        # read docx
        doc = docx.Document(io.BytesIO(decoded))
        parsed_resume = '\n\n'.join([paragraph.text for paragraph in doc.paragraphs])
        experiences = extract_experiences(parsed_resume)
        skills = extract_skills(parsed_resume)
        return "EXPERIENCE: " + experiences + "\n\n" + "SKILLS: " + skills  
    else:
        return 'Invalid file type'

@app.callback(
    Output('output_area','value'), 
    Input('file_upload', 'contents'),
    Input('file_upload', 'filename'),
    )
def update_output(contents, filename):
    if contents is not None:
        return parse_contents(contents, filename)


if __name__ == "__main__":
    app.run_server(debug=True)

