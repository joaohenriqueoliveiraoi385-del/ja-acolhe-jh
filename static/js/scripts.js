function alternarComentarios(botao) {
    const blocoComentarios = botao.nextElementSibling;
    blocoComentarios.classList.toggle('ativo');

    const matchQtd = botao.textContent.match(/\d+/);
    const qtdTotal = matchQtd ? matchQtd[0] : "0";

    if (blocoComentarios.classList.contains('ativo')) {
        botao.innerHTML = `💬 Ocultar comentários (${qtdTotal})`;
    } else {
        botao.innerHTML = `💬 Mostrar comentários (${qtdTotal})`;
    }
}