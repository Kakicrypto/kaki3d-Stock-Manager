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
        
        <button id="scan-btn" style="...">Lancer le scan</button>

        <div id="nfc-result" style="display: none;">
            <p id="nfc-uid"></p>
        </div>
    </div>

        <script>
        // 2. La logique (JavaScript) bien séparée
        document.getElementById('scan-btn').addEventListener('click', async () => {
            alert("1 - fonction démarrée");
            // Note: Assure-toi que startNFCScan() est définie ici aussi !
            if (typeof startNFCScan === 'function') {
                await startNFCScan();
            }
        });
        </script>
        
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

    async function startNFCScan() {
        alert("1 - fonction démarrée");

        if (!('NDEFReader' in window)) {
            alert("2 - NDEFReader non supporté !");
            return;
        }

        alert("3 - NDEFReader disponible, tentative scan...");

        try {
            nfcReader = new NDEFReader();
            await nfcReader.scan();
            alert("4 - scan() réussi, en attente du tag !");

            nfcReader.addEventListener("reading", ({ message, serialNumber }) => {
                const uid = serialNumber.toUpperCase();
                alert("5 - Tag lu ! UID : " + uid);

                document.getElementById('nfc-uid').textContent = uid;
                document.getElementById('nfc-result').style.display = 'block';
                document.getElementById('nfc-status').textContent = '✅ Tag scanné : ' + uid;

                setTimeout(() => {
                    window.top.location.href = window.top.location.pathname + "?nfc_uid=" + uid;
                }, 1500);
            });

            nfcReader.addEventListener("readingerror", () => {
                alert("ERREUR de lecture du tag !");
            });

        } catch (error) {
            alert("ERREUR : " + error.name + " - " + error.message);
        }
    }

    window.addEventListener('message', function(event) {
        if (event.data && event.data.type === 'nfc_reset') {
            document.getElementById('nfc-result').style.display = 'none';
            document.getElementById('nfc-status').textContent = 'Prêt pour un nouveau scan';
        }
    });
    </script>
    """

    components.html(nfc_html, height=280, scrolling=False)