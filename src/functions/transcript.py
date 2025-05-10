import discord 

# FUNÇÃO PARA SALVAR AS INFORMAÇÔES DO TICKET EM UM ARQUIVO HTML
async def generate_transcript(ticket_data, user: discord.Member, channel_id: int):
    trasncript_channel = discord.utils.get(user.guild.channels, id=channel_id)
    
    user_name = ticket_data["user"]
    user_id = ticket_data["user_id"]
    created_at = ticket_data["data"].strftime("%Y-%m-%d %H:%M:%S")
    feedback = ticket_data["feedback"]
    nota = ticket_data["nota"]
    recomenda = ticket_data["recomenda"]
    staff_avalido = ticket_data["staff"]
    
    messages_html = ""
    for msg in ticket_data["messages"]:
        messages_html += f"<p><b>{msg['author']}:</b> {msg['content']} <i>({msg['timestamp']})</i></p>"
    
    html_content = f"""
    <html>
        <head>
            <title>Ticket - {user_name}</title>
            <style>
                /* Reset de estilos básicos */
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: #1e2a47;
                    color: #333;
                    line-height: 1.6;
                    padding: 30px 0;
                }}
                h1 {{
                    background-color: #007bff;
                    color: white;
                    text-align: center;
                    padding: 15px;
                    border-radius: 10px 10px 0 0;
                    margin-bottom: 20px;
                    font-size: 2em;
                    letter-spacing: 1px;
                }}
                h2 {{
                    color: #333;
                    margin-top: 20px;
                    font-size: 1.5em;
                    text-align: center;
                }}
                .container {{
                    width: 80%;
                    max-width: 900px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    transition: transform 0.3s ease, box-shadow 0.3s ease;
                }}
                .container:hover {{
                    transform: translateY(-5px);
                    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
                }}
                .ticket-info {{
                    background-color: #e9f1ff;
                    padding: 20px;
                    border-radius: 8px;
                    margin-bottom: 30px;
                    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
                }}
                .ticket-info b {{
                    color: #007bff;
                }}
                .messages {{
                    border-top: 2px solid #f1f1f1;
                    padding-top: 20px;
                }}
                .message {{
                    background-color: #f8f8f8;
                    padding: 15px;
                    margin-bottom: 15px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    transition: background-color 0.3s ease;
                }}
                .message:hover {{
                    background-color: #f1f1f1;
                }}
                .message b {{
                    color: #007bff;
                    font-weight: bold;
                }}
                .timestamp {{
                    font-size: 12px;
                    color: #888;
                    display: block;
                    margin-top: 5px;
                }}
                /* Botão interativo */
                .button {{
                    display: inline-block;
                    background-color: #28a745;
                    color: white;
                    padding: 12px 30px;
                    font-size: 16px;
                    border-radius: 8px;
                    text-align: center;
                    text-decoration: none;
                    cursor: pointer;
                    margin: 10px 0;
                    transition: background-color 0.3s ease, transform 0.2s ease;
                }}
                .button:hover {{
                    background-color: #218838;
                    transform: translateY(-3px);
                }}
                .button:active {{
                    transform: translateY(1px);
                }}
                /* Estilo para o footer */
                footer {{
                    text-align: center;
                    color: #777;
                    font-size: 14px;
                    margin-top: 40px;
                }}
                footer a {{
                    color: #007bff;
                    text-decoration: none;
                }}
                footer a:hover {{
                    text-decoration: underline;
                }}
            </style>
        </head>
        <body>
            <h1>📄 Histórico de Atendimento</h1>
            <div class="container">
                <div class="ticket-info">
                    <p><b>Cliente/Usuário:</b> {user_name} ({user_id})</p>
                    <p><b>Abertura:</b> {created_at}</p>
                    <p><b>Nota:</b> {nota}</p> <p><b>STAFF:</b> {staff_avalido}</p>
                    <p><b>Feedback:</b> {feedback}</p>
                    <p><b>Indica nosso escritório?</b> {recomenda}</p>
                </div>
                <h2>📨 Mensagens:</h2>
                <div class="messages">
                    {messages_html}
                </div>
            </div>
            <footer>
                <p>&copy; 2025 - Obrigado pela avaliação!</p>
            </footer>
        </body>
    </html>
    """ 

    file_name = f"ticket_{user_id}.html"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(html_content)

    try:
        await trasncript_channel.send(content=f"Histórico de ticket(Cliente: <@{user_id}>)", file=discord.File(file_name))
    except Exception as e:
        print(f"Erro ao enviar DM para {user.name}: {e}")