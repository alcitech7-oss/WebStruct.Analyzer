let dadosMapeados = [];
let ultimosResultados = [];
let totalElementos = 0;
let urlParaMapear = '';
let elementosCompletos = [];

function mostrarToast(mensagem, tipo = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = mensagem;
    toast.className = 'toast toast-' + tipo;
    toast.style.display = 'block';
    setTimeout(function() { toast.style.display = 'none'; }, 4000);
}

async function mapear() {
    const url = document.getElementById('urlInput').value.trim();
    if (!url) {
        mostrarToast('Digite uma URL!', 'error');
        return;
    }
    urlParaMapear = url;
    document.getElementById('confirmUrl').textContent = url;
    document.getElementById('confirmModal').style.display = 'flex';
}

async function confirmarMapeamento(confirmado) {
    document.getElementById('confirmModal').style.display = 'none';

    if (!confirmado) {
        document.getElementById('statusMapeamento').innerHTML = '❌ Mapeamento cancelado!';
        document.getElementById('statusMapeamento').style.color = '#f85149';
        mostrarToast('Mapeamento cancelado!', 'error');
        return;
    }

    const status = document.getElementById('statusMapeamento');
    const botao = document.getElementById('btnMapear');
    botao.disabled = true;
    botao.innerHTML = '⏳ Mapeando...';

    const progressoContainer = document.getElementById('progressoContainer');
    const sucessoContainer = document.getElementById('sucessoContainer');
    progressoContainer.style.display = 'block';
    sucessoContainer.style.display = 'none';

    const barra = document.getElementById('progressoBarra');
    const porcentagem = document.getElementById('progressoPorcentagem');
    const mensagem = document.getElementById('progressoMensagem');

    const fases = [
        { pct: 10, msg: 'Conectando ao site...' },
        { pct: 30, msg: 'Carregando página...' },
        { pct: 50, msg: 'Extraindo elementos...' },
        { pct: 70, msg: 'Processando dados...' },
        { pct: 90, msg: 'Finalizando...' }
    ];

    let progressoAtual = 0;
    for (let i = 0; i < fases.length; i++) {
        const fase = fases[i];
        while (progressoAtual < fase.pct) {
            progressoAtual += Math.random() * 2 + 1;
            if (progressoAtual > fase.pct) progressoAtual = fase.pct;
            const pct = Math.round(progressoAtual);
            barra.style.width = pct + '%';
            porcentagem.textContent = pct + '%';
            mensagem.textContent = fase.msg;
            await new Promise(function(r) { setTimeout(r, 80); });
        }
    }

    try {
        const response = await fetch('/mapear', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: urlParaMapear })
        });

        const data = await response.json();

        if (data.erro) {
            status.innerHTML = '❌ ' + data.erro;
            status.style.color = '#f85149';
            progressoContainer.style.display = 'none';
            mostrarToast('Erro ao mapear: ' + data.erro, 'error');
            return;
        }

        barra.style.width = '100%';
        porcentagem.textContent = '100%';
        mensagem.textContent = '✅ Mapeamento concluído!';

        dadosMapeados = data.todos || data.primeiros || [];
        elementosCompletos = dadosMapeados;
        totalElementos = data.total;

        document.getElementById('estatisticas').style.display = 'flex';
        document.getElementById('statTotal').textContent = data.total;
        document.getElementById('statTags').textContent = Object.keys(data.tags || {}).length;

        progressoContainer.style.display = 'none';
        sucessoContainer.style.display = 'block';
        document.getElementById('sucessoDetalhes').textContent = data.total + ' elementos encontrados';

        status.innerHTML = '✅ ' + data.total + ' elementos mapeados!';
        status.style.color = '#3fb950';
        mostrarToast('✅ ' + data.total + ' elementos mapeados com sucesso!', 'success');

        mostrarResultados(dadosMapeados);

    } catch (error) {
        status.innerHTML = '❌ Erro: ' + error.message;
        status.style.color = '#f85149';
        progressoContainer.style.display = 'none';
        mostrarToast('Erro: ' + error.message, 'error');
    } finally {
        botao.disabled = false;
        botao.innerHTML = '🚀 Mapear';
    }
}

function filtrarElementos() {
    const input = document.getElementById('searchInput');
    if (!input) return;
    
    const termo = input.value.toLowerCase().trim();
    const status = document.getElementById('searchStatus');
    const btnClear = document.getElementById('btnClear');

    if (termo.length > 0) {
        if (btnClear) btnClear.style.display = 'inline-block';
    } else {
        if (btnClear) btnClear.style.display = 'none';
    }

    if (termo === '') {
        mostrarResultados(elementosCompletos);
        if (status) {
            status.innerHTML = '📌 ' + elementosCompletos.length + ' elementos no total';
            status.style.color = '#8b949e';
        }
        return;
    }

    const filtrados = elementosCompletos.filter(function(elem) {
        const campos = [
            elem.tag || '',
            elem.classe || '',
            elem.id || '',
            elem.texto || '',
            elem.link || '',
            elem.seletor_css || '',
            elem.xpath || ''
        ];
        const textoCompleto = campos.join(' ').toLowerCase();
        return textoCompleto.includes(termo);
    });

    if (filtrados.length > 0) {
        mostrarResultados(filtrados);
        if (status) {
            status.innerHTML = '🔍 ' + filtrados.length + ' elementos encontrados para "' + termo + '"';
            status.style.color = '#3fb950';
        }
    } else {
        const lista = document.getElementById('resultadosLista');
        if (lista) {
            lista.innerHTML = `
                <div class="sem-resultados">
                    <span class="sem-icon">🔍</span>
                    <p>Nenhum elemento encontrado para <strong>"${termo}"</strong></p>
                    <p class="sem-dica">Tente buscar por: tag (div), classe (.header), ID (#menu) ou texto ("dólar")</p>
                </div>
            `;
        }
        if (status) {
            status.innerHTML = '❌ Nenhum resultado para "' + termo + '"';
            status.style.color = '#f85149';
        }
    }
}

function limparBusca() {
    const input = document.getElementById('searchInput');
    if (input) {
        input.value = '';
    }
    const btnClear = document.getElementById('btnClear');
    if (btnClear) btnClear.style.display = 'none';
    filtrarElementos();
}

function mostrarResultados(elementos) {
    if (elementos && elementos.length > 0 && 
        (elementos === dadosMapeados || elementos.length === dadosMapeados.length)) {
        elementosCompletos = elementos;
    }

    const estadoInicial = document.getElementById('estadoInicial');
    const lista = document.getElementById('resultadosLista');
    
    if (!elementos || elementos.length === 0) {
        if (estadoInicial) estadoInicial.style.display = 'flex';
        if (lista) lista.style.display = 'none';
        return;
    }
    
    if (estadoInicial) estadoInicial.style.display = 'none';
    if (lista) lista.style.display = 'block';
    
    const container = document.getElementById('resultadosContainer');
    let html = '<div class="lista-header">📌 ' + elementos.length + ' elementos</div><ul class="lista-elementos">';
    
    for (let i = 0; i < elementos.length; i++) {
        const elem = elementos[i];
        const texto = elem.texto ? elem.texto.slice(0, 60) : 'sem texto';
        const idx = elementosCompletos.indexOf(elem);
        const indexReal = idx >= 0 ? idx : 0;
        html += `
            <li onclick="mostrarModal(${indexReal})">
                <span class="tag">${elem.tag || '?'}</span>
                ${elem.classe ? '<span class="classe">.' + elem.classe.slice(0, 20) + '</span>' : ''}
                ${elem.id ? '<span class="id">#' + elem.id + '</span>' : ''}
                <span class="texto">"' + texto + '"</span>
                <span class="badge">🔍</span>
            </li>
        `;
    }
    html += '</ul>';
    
    container.innerHTML = `
        <div id="estadoInicial" class="estado-inicial" style="display:none;">
            <img src="/static/gif2.gif" alt="Mapeie um site" class="gif-placeholder">
            <h3>https://github.com/alcitech7-oss</h3>
            <p>Digite a URL acima e clique em <strong>"Mapear"</strong></p>
        </div>
        <div id="resultadosLista">${html}</div>
    `;
}

function mostrarModal(index) {
    const elemento = ultimosResultados[index] || dadosMapeados[index] || elementosCompletos[index];
    if (!elemento) return;

    const body = document.getElementById('modalBody');
    let html = `
        <div class="detalhe-item"><label>Tag</label><code>${elemento.tag || 'N/A'}</code></div>
        <div class="detalhe-item"><label>Classe</label><code>${elemento.classe || '(nenhuma)'}</code></div>
        <div class="detalhe-item"><label>ID</label><code>${elemento.id || '(nenhum)'}</code></div>
        <div class="detalhe-item">
            <label>Seletor CSS</label>
            <code>${elemento.seletor_css || 'N/A'}</code>
            <button class="btn-copiar" onclick="copiarSeletor('${elemento.seletor_css}', 'CSS')">📋 Copiar</button>
        </div>
        <div class="detalhe-item">
            <label>XPath</label>
            <code>${elemento.xpath || 'N/A'}</code>
            <button class="btn-copiar" onclick="copiarSeletor('${elemento.xpath}', 'XPath')">📋 Copiar</button>
        </div>
        <div class="detalhe-item">
            <label>Código Playwright</label>
            <code>${gerarCodigoPlaywright(elemento)}</code>
            <button class="btn-copiar" onclick="copiarSeletor('${gerarCodigoPlaywright(elemento)}', 'Playwright')">📋 Copiar</button>
        </div>
    `;
    if (elemento.texto) html += '<div class="detalhe-item"><label>Texto</label><code>' + elemento.texto + '</code></div>';
    if (elemento.link) html += '<div class="detalhe-item"><label>Link</label><code>' + elemento.link + '</code></div>';

    body.innerHTML = html;
    document.getElementById('elementoModal').style.display = 'flex';
}

function gerarCodigoPlaywright(elemento) {
    if (elemento.seletor_css && elemento.seletor_css !== 'N/A') return 'page.locator("' + elemento.seletor_css + '")';
    if (elemento.xpath && elemento.xpath !== 'N/A') return 'page.locator("xpath=' + elemento.xpath + '")';
    return '# Seletor não disponível';
}

function copiarSeletor(texto, tipo) {
    if (!texto || texto === 'N/A' || texto === '# Seletor não disponível') {
        mostrarToast('Não há seletor para copiar', 'error');
        return;
    }
    navigator.clipboard.writeText(texto).then(function() {
        const botoes = document.querySelectorAll('.btn-copiar');
        for (let i = 0; i < botoes.length; i++) {
            const b = botoes[i];
            if (b.innerText.includes(tipo) || b.innerText.includes('📋')) {
                const original = b.innerText;
                b.innerText = '✅ Copiado!';
                b.classList.add('copiado');
                setTimeout(function() { b.innerText = original; b.classList.remove('copiado'); }, 2000);
            }
        }
        mostrarToast('✅ Seletor copiado!', 'success');
    }).catch(function() { mostrarToast('Copie manualmente: Ctrl+C', 'error'); });
}

function fecharModal() {
    document.getElementById('elementoModal').style.display = 'none';
}

async function exportar(formato) {
    try {
        const response = await fetch('/exportar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ formato: formato })
        });

        if (!response.ok) {
            const erro = await response.json();
            throw new Error(erro.erro || 'Erro ao exportar');
        }

        const blob = await response.blob();

        if ('showSaveFilePicker' in window) {
            try {
                const extensoes = { 'excel': '.xlsx', 'json': '.json', 'csv': '.csv' };
                const handle = await window.showSaveFilePicker({
                    suggestedName: 'mapa_' + Date.now() + extensoes[formato],
                    types: [{
                        description: formato.toUpperCase() + ' file',
                        accept: { 'application/octet-stream': [extensoes[formato]] }
                    }]
                });

                const writable = await handle.createWritable();
                await writable.write(blob);
                await writable.close();

                mostrarToast('✅ ' + formato.toUpperCase() + ' salvo com sucesso!', 'success');
                return;
            } catch (err) {
                if (err.name === 'AbortError' || err.name === 'SecurityError') {
                    mostrarToast('⏹️ Salvamento cancelado', 'info');
                    return;
                }
                console.warn('Fallback para download automático:', err);
            }
        }

        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'mapa_' + Date.now() + '.' + (formato === 'excel' ? 'xlsx' : formato);
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

        mostrarToast('📥 ' + formato.toUpperCase() + ' baixado!', 'success');

    } catch (error) {
        mostrarToast('❌ Erro: ' + error.message, 'error');
        console.error(error);
    }
}

function mostrarEstadoInicial() {
    const container = document.getElementById('resultadosContainer');
    const estadoInicial = document.getElementById('estadoInicial');
    const lista = document.getElementById('resultadosLista');
    
    if (estadoInicial) {
        estadoInicial.style.display = 'flex';
        if (lista) lista.style.display = 'none';
        return;
    }
    
    container.innerHTML = `
        <div id="estadoInicial" class="estado-inicial">
            <img src="/static/gif2.gif" alt="Mapeie um site" class="gif-placeholder">
            <h3>https://github.com/alcitech7-oss</h3>
            <p>Digite a URL acima e clique em <strong>"Mapear"</strong></p>
        </div>
        <div id="resultadosLista" style="display: none;"></div>
    `;
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('urlInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') mapear();
    });
    
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') fecharModal();
    });
    
    var modal = document.getElementById('elementoModal');
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === this) fecharModal();
        });
    }
    
    var confirmModal = document.getElementById('confirmModal');
    if (confirmModal) {
        confirmModal.addEventListener('click', function(e) {
            if (e.target === this) {
                document.getElementById('confirmModal').style.display = 'none';
                mostrarToast('Mapeamento cancelado', 'error');
            }
        });
    }
    
    mostrarEstadoInicial();
    console.log('✅ Struct Analyzer PRO carregado!');
});