(function () {
    const socket = new WebSocket('ws://' + window.location.host + '/ws/admin/orders/');

    socket.onmessage = function (e) {
        const data = JSON.parse(e.data);

        if (data.type === 'new_order') {
            showBanner(data.message);
        }
    };

    function showBanner(message) {
        // Vérifie si la bannière est déjà affichée
        if (document.getElementById('new-order-banner')) return;

        const banner = document.createElement('div');
        banner.id = 'new-order-banner';
        banner.innerHTML = `
            <div style="
                background: #ffecec;
                color: #900;
                padding: 12px;
                text-align: center;
                font-weight: bold;
                border-bottom: 1px solid #ddd;
                z-index: 1000;
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
            ">
                ${message}
                <button id="reload-orders-btn" style="
                    margin-left: 20px;
                    padding: 6px 12px;
                    background: #900;
                    color: #fff;
                    border: none;
                    cursor: pointer;
                ">
                    Charger les nouvelles commandes
                </button>
            </div>
        `;

        document.body.prepend(banner);

        // Ajoute le clic sur le bouton
        document.getElementById('reload-orders-btn').addEventListener('click', function () {
            fetch('/orders/refresh-badge/')
                .then(response => response.json())
                .then(data => {
                    // Exemple : met à jour le label du menu
                    const ordersMenu = document.querySelector('[href="/admin/orders/"]');
                    if (ordersMenu && data.count > 0) {
                        ordersMenu.innerText = `Orders 🔴 ${data.count}`;
                    }

                    // Supprime la bannière
                    banner.remove();
                });
        });
    }
})();
