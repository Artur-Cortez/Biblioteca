function sendToPython(data) {
    const jsonData = JSON.stringify(data);
    const event = new Event("customEvent");
    event.data = jsonData;
    document.dispatchEvent(event);
}

function botao_clique(title, author, cover_image_url, categories, data_publicacao) {
    const dicionario = {
        "titulo": title,
        "autor": author,
        "img": cover_image_url,
        "categories": categories,
        "data_publicacao": data_publicacao
    };

    sendToPython(dicionario);
}