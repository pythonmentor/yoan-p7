"""this file test all function's view"""
from grandpyapp import view, parser, place, wiki
import pytest
import json

def test_index(monkeypatch):
    """test than index function return correctly html and mock render_template function"""
    index_html = """
                <html>
                    <body>
                        <div>AIzaSyBkuQqSZkEBSmlSbeBOw_yr9G_GTayiwks</div>
                        <div>openclassrooms</div>
                        <div>path/to/css</div>
                        <div>path/to/css</div>
                        <div>path/to/css</div>
                    </body>
                </html>
                """

    def mock_template_render(request, *args, **kwargs):
        variable_to_html_elt = ""
        for key in kwargs:
            # print(kwargs[key])

            if key == 'api_key':
                variable_to_html_elt += f"""    <div>AIzaSyBkuQqSZkEBSmlSbeBOw_yr9G_GTayiwks</div>"""
                
            else:
                variable_to_html_elt += f"""
                        <div>{kwargs[key]}</div>"""
            
        return f"""
                <html>
                    <body>
                    {variable_to_html_elt}
                    </body>
                </html>
                """

    def mock_url_for(request, *args, **kwargs):
        return "path/to/css"

    monkeypatch.setattr(view, "render_template", mock_template_render)
    monkeypatch.setattr(view, 'url_for', mock_url_for)

    render = view.index()
    assert index_html == render


class MockResponse:

    @staticmethod
    def google_json():
        return {'candidates': [{'formatted_address': '7 Cité Paradis, 75010 Paris, France'}]}
    
    @staticmethod
    def wiki_json():
        return {"je ne connais pas la reponse": "mais je sais qu'elle est en json"}


def test_get_data(monkeypatch):
    """test than response wiki return correctly the wiki data when she receive an answer"""
    answer = "Ou se situe openclassrooms"

    def mock_find_keyword(*args, **kwargs):
        keyword_from_answer = "openclassrooms"
        return keyword_from_answer

    def mock_google_place(*args, **kwargs):
        return MockResponse().google_json()

    def mock_wiki(*args, **kwargs):
        return MockResponse().wiki_json()

    monkeypatch.setattr(parser.Parser, 'find_keyword', mock_find_keyword)
    monkeypatch.setattr(place.QueryPlace, 'find_place', mock_google_place)
    monkeypatch.setattr(wiki.Wiki, 'find_data_about_place', mock_wiki)

    # response_result = {
    #     "resp_google":
    #     {
    #         "candidates": [
    #             {
    #                 "formatted_address": "7 Cité Paradis, 75010 Paris, France",
    #             }
    #         ]
    #     },
    #     "resp_wiki":
    #     {
    #         "je ne connais pas la reponse": "mais je sais qu'elle est en json"
    #     }
    # }

    print('test = ', view.get_data(answer))
    assert view.get_data(answer) == {'candidates': [{'formatted_address': '7 Cité Paradis, 75010 Paris, France'}]}
