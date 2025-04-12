document.addEventListener('DOMContentLoaded', function () {
    // Mobile Navigation Toggle
    const navbarToggle = document.querySelector('.navbar-toggle');
    const navbarMenu = document.querySelector('.navbar-menu');
    const closeNavBtn = document.createElement('button');

    closeNavBtn.classList.add('close-nav');
    closeNavBtn.innerHTML = '<i class="fas fa-times"></i>';
    closeNavBtn.style.position = 'absolute';
    closeNavBtn.style.top = '20px';
    closeNavBtn.style.right = '20px';
    closeNavBtn.style.background = 'none';
    closeNavBtn.style.fontSize = '24px';
    closeNavBtn.style.border = 'none';
    closeNavBtn.style.cursor = 'pointer';

    navbarMenu.prepend(closeNavBtn);

    navbarToggle.addEventListener('click', function () {
        navbarMenu.classList.add('active');
        document.body.style.overflow = 'hidden';
    });

    closeNavBtn.addEventListener('click', function () {
        navbarMenu.classList.remove('active');
        document.body.style.overflow = '';
    });

    document.addEventListener('click', function (event) {
        if (
            navbarMenu.classList.contains('active') &&
            !navbarMenu.contains(event.target) &&
            !navbarToggle.contains(event.target)
        ) {
            navbarMenu.classList.remove('active');
            document.body.style.overflow = '';
        }
    });

    // Filter Sidebar Toggle
    const filterToggleBtn = document.getElementById('filterToggleBtn');
    const filtersSidebar = document.querySelector('.filters-sidebar');
    const closeFiltersBtn = document.querySelector('.close-filters');

    if (filterToggleBtn && filtersSidebar && closeFiltersBtn) {
        filterToggleBtn.addEventListener('click', function () {
            filtersSidebar.classList.add('active');
            document.body.style.overflow = 'hidden';
        });

        closeFiltersBtn.addEventListener('click', function () {
            filtersSidebar.classList.remove('active');
            document.body.style.overflow = '';
        });
    }

    // Quick View Modal
    const quickViewButtons = document.querySelectorAll('.quickview-btn');
    quickViewButtons.forEach(button => {
        button.addEventListener('click', function () {
            const productCard = this.closest('.product-card');
            const productImage = productCard.querySelector('.product-image img').src;
            const productTitle = productCard.querySelector('.product-title').textContent;
            const productPrice = productCard.querySelector('.current-price').textContent;
            const productDescription = productCard.querySelector('.product-description').textContent;

            const modal = document.createElement('div');
            modal.classList.add('quick-view-modal');
            modal.innerHTML = `
                <div class="quick-view-content">
                    <button class="close-modal"><i class="fas fa-times"></i></button>
                    <div class="modal-grid">
                        <div class="modal-image">
                            <img src="${productImage}" alt="${productTitle}">
                        </div>
                        <div class="modal-info">
                            <h3 style="font-size: 24px; font-weight: 600; margin-bottom: 10px;">${productTitle}</h3>
                            <p class="modal-price" style="font-size: 18px; font-weight: 500; color: #ff5252; margin-bottom: 15px;">${productPrice}</p>
                            <div class="modal-divider" style="height: 1px; background-color: #eee; margin: 20px 0;"></div>
                            <p class="modal-description" style="font-size: 15px; color: #555; line-height: 1.6;">${productDescription}</p>
                        </div>
                    </div>
                </div>
            `;

            modal.style.position = 'fixed';
            modal.style.top = '0';
            modal.style.left = '0';
            modal.style.width = '100%';
            modal.style.height = '100%';
            modal.style.backgroundColor = 'rgba(0,0,0,0.5)';
            modal.style.display = 'flex';
            modal.style.alignItems = 'center';
            modal.style.justifyContent = 'center';
            modal.style.zIndex = '2000';

            const modalContent = modal.querySelector('.quick-view-content');
            modalContent.style.backgroundColor = 'white';
            modalContent.style.borderRadius = '12px';
            modalContent.style.maxWidth = '900px';
            modalContent.style.width = '90%';
            modalContent.style.maxHeight = '90vh';
            modalContent.style.overflow = 'auto';
            modalContent.style.position = 'relative';
            modalContent.style.boxShadow = '0 10px 25px rgba(0,0,0,0.2)';

            const modalGrid = modal.querySelector('.modal-grid');
            modalGrid.style.display = 'grid';
            modalGrid.style.gridTemplateColumns = 'repeat(auto-fit, minmax(300px, 1fr))';
            modalGrid.style.gap = '30px';
            modalGrid.style.padding = '30px';

            const modalImage = modal.querySelector('.modal-image img');
            modalImage.style.width = '100%';
            modalImage.style.borderRadius = '10px';

            const closeModal = modal.querySelector('.close-modal');
            closeModal.style.position = 'absolute';
            closeModal.style.top = '15px';
            closeModal.style.right = '15px';
            closeModal.style.background = 'none';
            closeModal.style.border = 'none';
            closeModal.style.fontSize = '22px';
            closeModal.style.cursor = 'pointer';
            closeModal.style.color = '#555';

            closeModal.addEventListener('click', () => {
                document.body.removeChild(modal);
                document.body.style.overflow = '';
            });

            modal.addEventListener('click', (event) => {
                if (event.target === modal) {
                    document.body.removeChild(modal);
                    document.body.style.overflow = '';
                }
            });

            document.body.appendChild(modal);
            document.body.style.overflow = 'hidden';
        });
    });

    // Reset filters
    window.resetFilters = function () {
        window.location.href = window.location.pathname;
    };
});
