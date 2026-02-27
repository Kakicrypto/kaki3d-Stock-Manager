# nfc_scanner.py
# Composant NFC pour Streamlit - utilise la Web NFC API (Android Chrome uniquement)

import streamlit.components.v1 as components

def nfc_scanner_component():
    """
    Injecte un composant HTML/JS qui utilise la Web NFC API.
    Retourne l'UID NFC scanné, ou None si pas encore scanné.
    
    ⚠️  Compatible uniquement avec : Android + Chrome (ou Chromium)
    ⚠️  Nécessite HTTPS (ou localhost pour les tests)
    """

    nfc_html = """
    <div id="nfc-container" style="
        background: linear-gradient(135deg, #1e2a38, #2e3f52);
        border: 2px dashed #4CAF50;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        font-family: 'Segoe UI', sans-serif;
        color: white;
        margin: 10px 0;
    ">
        <div style="font-size: 48px; margin-bottom: 8px;">📡</div>
        <h3 style="margin: 0 0 8px 0; color: #4CAF50;">Scanner un Tag NFC</h3>
        <p id="nfc-status" style="color: #aaa; font-size: 14px; margin: 0 0 16px 0;">
            Appuie sur le bouton, puis approche ton tag NFC
        </p>
        
        <button id="scan-btn" onclick="startNFCScan()" style="
            background: #4CAF50;
            color: white;
            border: none;
            padding: 12px 28px;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: background 0.2s;
        ">
            🔍 Démarrer le scan
        </button>
        
        <div id="nfc-result" style="
            display: none;
            margin-top: 16px;
            background: rgba(76, 175, 80, 0.2);
            border: 1px solid #4CAF50;
            border-radius: 8px;
            padding: 12px;
        ">
            <p style="margin: 0; font-size: 13px; color: #aaa;">UID détecté :</p>
            <p id="nfc-uid" style="margin: 4px 0 0 0; font-size: 18px; font-weight: bold; color: #4CAF50; font-family: monospace;"></p>
        </div>

        <div id="nfc-error" style="
            display: none;
            margin-top: 16px;
            background: rgba(244, 67, 54, 0.15);
            border: 1px solid #f44336;
            border-radius: 8px;
            padding: 12px;
            color: #ff7961;
            font-size: 14px;
        "></div>
    </div>

    <script>
    let nfcReader = null;
    let isScanning = false;

    async function startNFCScan() {
        const statusEl = document.getElementById('nfc-status');
        const btnEl = document.getElementById('scan-btn');
        const resultEl = document.getElementById('nfc-result');
        const errorEl = document.getElementById('nfc-error');
        const uidEl = document.getElementById('nfc-uid');

        // Reset
        resultEl.style.display = 'none';
        errorEl.style.display = 'none';

        // Vérifie si Web NFC est dispo
        if (!('NDEFReader' in window)) {
            errorEl.style.display = 'block';
            errorEl.innerHTML = '❌ Web NFC non supporté sur ce navigateur.<br><small>Utilise Chrome sur Android.</small>';
            return;
        }

        try {
            btnEl.disabled = true;
            btnEl.style.background = '#888';
            statusEl.textContent = '📡 En attente du tag NFC... (approche-le)';
            statusEl.style.color = '#FFD700';

            nfcReader = new NDEFReader();
            await nfcReader.scan();

            nfcReader.addEventListener("reading", ({ message, serialNumber }) => {
                const uid = serialNumber.toUpperCase();
                
                // Affichage résultat
                uidEl.textContent = uid;
                resultEl.style.display = 'block';
                statusEl.textContent = '✅ Tag scanné avec succès !';
                statusEl.style.color = '#4CAF50';
                btnEl.disabled = false;
                btnEl.style.background = '#4CAF50';
                btnEl.textContent = '🔄 Scanner un autre';

                // Envoi vers Streamlit via postMessage
                window.parent.postMessage({
                    type: 'nfc_scanned',
                    uid: uid
                }, '*');
            });

            nfcReader.addEventListener("readingerror", () => {
                errorEl.style.display = 'block';
                errorEl.textContent = '⚠️ Erreur de lecture. Réessaie.';
                btnEl.disabled = false;
                btnEl.style.background = '#4CAF50';
            });

        } catch (error) {
            errorEl.style.display = 'block';
            if (error.name === 'NotAllowedError') {
                errorEl.innerHTML = '🔒 Permission NFC refusée.<br><small>Autorise l\'accès NFC dans ton navigateur.</small>';
            } else {
                errorEl.innerHTML = '❌ Erreur : ' + error.message;
            }
            btnEl.disabled = false;
            btnEl.style.background = '#4CAF50';
            statusEl.textContent = 'Appuie sur le bouton, puis approche ton tag NFC';
            statusEl.style.color = '#aaa';
        }
    }

    // Écoute le postMessage de l'iframe parente (pour debug / futures extensions)
    window.addEventListener('message', function(event) {
        if (event.data && event.data.type === 'nfc_reset') {
            document.getElementById('nfc-result').style.display = 'none';
            document.getElementById('nfc-status').textContent = 'Prêt pour un nouveau scan';
        }
    });
    </script>
    """

    # On injecte le composant et on écoute via st.components
    # La hauteur est fixe, ajuste si besoin
    components.html(nfc_html, height=280, scrolling=False)