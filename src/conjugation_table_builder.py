"""Conjugation table builder — generates visual reference tables for Italian verbs."""

from __future__ import annotations

from .verb_conjugator import ConjugationData


class ConjugationTableError(Exception):
    """Raised when conjugation table generation fails."""


class ConjugationTableBuilder:
    """Generates visual conjugation reference tables from conjugation data."""

    def build_html_table(self, data: ConjugationData) -> str:
        """Generate an HTML conjugation table for the verb.
        
        Returns a complete HTML page with a styled conjugation table.
        """
        html = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Conjugazione: {data.infinitive}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            background-color: #f8f9fa;
            color: #333;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 40px;
        }}
        
        .verb-title {{
            font-size: 2.5em;
            color: #2c3e50;
            margin-bottom: 10px;
            font-weight: 300;
        }}
        
        .subtitle {{
            color: #7f8c8d;
            font-size: 1.1em;
        }}
        
        .conjugation-table {{
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            margin-bottom: 30px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            font-size: 1.1em;
        }}
        
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #ecf0f1;
        }}
        
        .person {{
            font-weight: 600;
            color: #2c3e50;
            width: 120px;
        }}
        
        .conjugation {{
            font-size: 1.1em;
            color: #27ae60;
            font-weight: 500;
        }}
        
        .tense-section {{
            margin-bottom: 25px;
        }}
        
        .tense-title {{
            background: #34495e;
            color: white;
            padding: 10px 15px;
            margin: 0;
            font-size: 1.2em;
            font-weight: 600;
        }}
        
        tr:hover {{
            background-color: #f8f9fa;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            color: #7f8c8d;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1 class="verb-title">{data.infinitive}</h1>
        <p class="subtitle">Tavola di Coniugazione</p>
    </div>

    <div class="tense-section">
        <div class="conjugation-table">
            <h2 class="tense-title">Presente Indicativo</h2>
            <table>
                <tbody>
                    <tr>
                        <td class="person">io</td>
                        <td class="conjugation">{data.present_io}</td>
                    </tr>
                    <tr>
                        <td class="person">tu</td>
                        <td class="conjugation">{data.present_tu}</td>
                    </tr>
                    <tr>
                        <td class="person">lui/lei</td>
                        <td class="conjugation">{data.present_lui_lei}</td>
                    </tr>
                    <tr>
                        <td class="person">noi</td>
                        <td class="conjugation">{data.present_noi}</td>
                    </tr>
                    <tr>
                        <td class="person">voi</td>
                        <td class="conjugation">{data.present_voi}</td>
                    </tr>
                    <tr>
                        <td class="person">loro</td>
                        <td class="conjugation">{data.present_loro}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <div class="tense-section">
        <div class="conjugation-table">
            <h2 class="tense-title">Passato Prossimo</h2>
            <table>
                <tbody>
                    <tr>
                        <td class="person">io</td>
                        <td class="conjugation">{data.past_io}</td>
                    </tr>
                    <tr>
                        <td class="person">tu</td>
                        <td class="conjugation">{data.past_tu}</td>
                    </tr>
                    <tr>
                        <td class="person">lui/lei</td>
                        <td class="conjugation">{data.past_lui_lei}</td>
                    </tr>
                    <tr>
                        <td class="person">noi</td>
                        <td class="conjugation">{data.past_noi}</td>
                    </tr>
                    <tr>
                        <td class="person">voi</td>
                        <td class="conjugation">{data.past_voi}</td>
                    </tr>
                    <tr>
                        <td class="person">loro</td>
                        <td class="conjugation">{data.past_loro}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <div class="tense-section">
        <div class="conjugation-table">
            <h2 class="tense-title">Futuro Semplice</h2>
            <table>
                <tbody>
                    <tr>
                        <td class="person">io</td>
                        <td class="conjugation">{data.future_io}</td>
                    </tr>
                    <tr>
                        <td class="person">tu</td>
                        <td class="conjugation">{data.future_tu}</td>
                    </tr>
                    <tr>
                        <td class="person">lui/lei</td>
                        <td class="conjugation">{data.future_lui_lei}</td>
                    </tr>
                    <tr>
                        <td class="person">noi</td>
                        <td class="conjugation">{data.future_noi}</td>
                    </tr>
                    <tr>
                        <td class="person">voi</td>
                        <td class="conjugation">{data.future_voi}</td>
                    </tr>
                    <tr>
                        <td class="person">loro</td>
                        <td class="conjugation">{data.future_loro}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <div class="footer">
        <p>Generato con Italian Learning Workflow</p>
    </div>
</body>
</html>"""
        
        return html