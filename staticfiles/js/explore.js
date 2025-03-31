// Main JavaScript for A&K Accessories And Closet

document.addEventListener('DOMContentLoaded', function() {
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

    navbarToggle.addEventListener('click', function() {
        navbarMenu.classList.add('active');
        document.body.style.overflow = 'hidden';
    });

    closeNavBtn.addEventListener('click', function() {
        navbarMenu.classList.remove('active');
        document.body.style.overflow = '';
    });

    // Close menu when clicking outside
    document.addEventListener('click', function(event) {
        if (navbarMenu.classList.contains('active') &&
            !navbarMenu.contains(event.target) &&
            !navbarToggle.contains(event.target)) {
            navbarMenu.classList.remove('active');
            document.body.style.overflow = '';
        }
    });

    // Filter sidebar toggle for mobile
    const filterToggleBtn = document.getElementById('filterToggleBtn');
    const filtersSidebar = document.querySelector('.filters-sidebar');
    const closeFiltersBtn = document.querySelector('.close-filters');

    if (filterToggleBtn && filtersSidebar && closeFiltersBtn) {
        filterToggleBtn.addEventListener('click', function() {
            filtersSidebar.classList.add('active');
            document.body.style.overflow = 'hidden';
        });

        closeFiltersBtn.addEventListener('click', function() {
            filtersSidebar.classList.remove('active');
            document.body.style.overflow = '';
        });
    }

    // Add to Cart functionality
    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
    const cartCount = document.querySelector('.cart-count');

    let cartItems = localStorage.getItem('cartItems') ? parseInt(localStorage.getItem('cartItems')) : 0;

    // Update cart count display
    if (cartCount) {
        cartCount.textContent = cartItems;
    }

    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            cartItems++;

            if (cartCount) {
                cartCount.textContent = cartItems;
            }

            localStorage.setItem('cartItems', cartItems);

            // Create and show add to cart notification
            const notification = document.createElement('div');
            notification.classList.add('cart-notification');
            notification.innerHTML = '<i class="fas fa-check-circle"></i> Item added to cart!';

            notification.style.position = 'fixed';
            notification.style.bottom = '20px';
            notification.style.right = '20px';
            notification.style.backgroundColor = '#28a745';
            notification.style.color = 'white';
            notification.style.padding = '10px 20px';
            notification.style.borderRadius = '5px';
            notification.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
            notification.style.zIndex = '1000';
            notification.style.display = 'flex';
            notification.style.alignItems = 'center';
            notification.style.gap = '10px';

            document.body.appendChild(notification);

            setTimeout(() => {
                notification.style.opacity = '0';
                notification.style.transition = 'opacity 0.5s ease';
                setTimeout(() => {
                    document.body.removeChild(notification);
                }, 500);
            }, 2000);
        });
    });

    // Wishlist functionality
    const wishlistButtons = document.querySelectorAll('.wishlist-btn');

    wishlistButtons.forEach(button => {
        button.addEventListener('click', function() {
            const icon = this.querySelector('i');

            if (icon.classList.contains('far')) {
                icon.classList.remove('far');
                icon.classList.add('fas');
                icon.style.color = '#e91e63';

                // Show wishlist notification
                showNotification('Added to wishlist!', '#e91e63');
            } else {
                icon.classList.remove('fas');
                icon.classList.add('far');
                icon.style.color = '';

                // Show wishlist removed notification
                showNotification('Removed from wishlist', '#6c757d');
            }
        });
    });

    // Quick view functionality
    const quickViewButtons = document.querySelectorAll('.quickview-btn');

    quickViewButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productCard = this.closest('.product-card');
            const productImage = productCard.querySelector('.product-image img').src;
            const productTitle = productCard.querySelector('.product-title').textContent;
            const productPrice = productCard.querySelector('.current-price').textContent;
            const productDescription = productCard.querySelector('.product-description').textContent;

            // Create modal
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
                            <h3>${productTitle}</h3>
                            <p class="modal-price">${productPrice}</p>
                            <div class="modal-divider"></div>
                            <p class="modal-description">${productDescription}</p>
                            <div class="modal-divider"></div>
                            <div class="modal-size">
                                <h4>Size:</h4>
                                <div class="size-options">
                                    <label class="size-option">
                                        <input type="radio" name="modal-size" value="S">
                                        <span>S</span>
                                    </label>
                                    <label class="size-option">
                                        <input type="radio" name="modal-size" value="M">
                                        <span>M</span>
                                    </label>
                                    <label class="size-option">
                                        <input type="radio" name="modal-size" value="L">
                                        <span>L</span>
                                    </label>
                                    <label class="size-option">
                                        <input type="radio" name="modal-size" value="XL">
                                        <span>XL</span>
                                    </label>
                                </div>
                            </div>
                            <div class="modal-quantity">
                                <h4>Quantity:</h4>
                                <div class="quantity-selector">
                                    <button class="quantity-btn minus">-</button>
                                    <input type="number" value="1" min="1" max="10">
                                    <button class="quantity-btn plus">+</button>
                                </div>
                            </div>
                            <div class="modal-actions">
                                <button class="btn add-to-cart-btn">Add to Cart</button>
                                <button class="btn btn-secondary wishlist-btn">
                                    <i class="far fa-heart"></i> Add to Wishlist
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `;

            // Style modal
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
            modalContent.style.borderRadius = '8px';
            modalContent.style.maxWidth = '900px';
            modalContent.style.width = '90%';
            modalContent.style.maxHeight = '90vh';
            modalContent.style.overflow = 'auto';
            modalContent.style.position = 'relative';

            const closeModal = modal.querySelector('.close-modal');
            closeModal.style.position = 'absolute';
            closeModal.style.top = '15px';
            closeModal.style.right = '15px';
            closeModal.style.background = 'none';
            closeModal.style.border = 'none';
            closeModal.style.fontSize = '20px';
            closeModal.style.cursor = 'pointer';
            closeModal.style.zIndex = '1';

            const modalGrid = modal.querySelector('.modal-grid');
            modalGrid.style.display = 'grid';
            modalGrid.style.gridTemplateColumns = 'repeat(auto-fit, minmax(300px, 1fr))';
            modalGrid.style.gap = '30px';
            modalGrid.style.padding = '30px';

            const modalImage = modal.querySelector('.modal-image img');
            modalImage.style.width = '100%';
            modalImage.style.height = 'auto';
            modalImage.style.borderRadius = '5px';

            const modalDividers = modal.querySelectorAll('.modal-divider');
            modalDividers.forEach(divider => {
                divider.style.height = '1px';
                divider.style.width = '100%';
                divider.style.backgroundColor = '#dee2e6';
                divider.style.margin = '20px 0';
            });

            const modalQuantity = modal.querySelector('.quantity-selector');
            modalQuantity.style.display = 'flex';
            modalQuantity.style.alignItems = 'center';
            modalQuantity.style.marginTop = '10px';
            modalQuantity.style.marginBottom = '20px';

            const quantityInput = modalQuantity.querySelector('input');
            quantityInput.style.width = '50px';
            quantityInput.style.textAlign = 'center';
            quantityInput.style.border = '1px solid #dee2e6';
            quantityInput.style.padding = '5px';

            const quantityBtns = modalQuantity.querySelectorAll('.quantity-btn');
            quantityBtns.forEach(btn => {
                btn.style.width = '30px';
                btn.style.height = '30px';
                btn.style.border = '1px solid #dee2e6';
                btn.style.background = 'none';
                btn.style.cursor = 'pointer';
            });

            const modalActions = modal.querySelector('.modal-actions');
            modalActions.style.display = 'flex';
            modalActions.style.gap = '10px';
            modalActions.style.marginTop = '20px';

            document.body.appendChild(modal);
            document.body.style.overflow = 'hidden';

            // Close modal functionality
            closeModal.addEventListener('click', function() {
                document.body.removeChild(modal);
                document.body.style.overflow = '';
            });

            // Close when clicking outside modal content
            modal.addEventListener('click', function(event) {
                if (event.target === modal) {
                    document.body.removeChild(modal);
                    document.body.style.overflow = '';
                }
            });

            // Quantity buttons
            const minusBtn = modal.querySelector('.minus');
            const plusBtn = modal.querySelector('.plus');

            minusBtn.addEventListener('click', function() {
                let value = parseInt(quantityInput.value);
                if (value > 1) {
                    quantityInput.value = value - 1;
                }
            });

            plusBtn.addEventListener('click', function() {
                let value = parseInt(quantityInput.value);
                if (value < 10) {
                    quantityInput.value = value + 1;
                }
            });

            // Modal add to cart button
            const modalAddToCartBtn = modal.querySelector('.add-to-cart-btn');
            modalAddToCartBtn.addEventListener('click', function() {
                cartItems += parseInt(quantityInput.value);

                if (cartCount) {
                    cartCount.textContent = cartItems;
                }

                localStorage.setItem('cartItems', cartItems);

                // Close modal
                document.body.removeChild(modal);
                document.body.style.overflow = '';

                // Show notification
                showNotification(`${quantityInput.value} item(s) added to cart!`, '#28a745');
            });

            // Modal wishlist button
            const modalWishlistBtn = modal.querySelector('.wishlist-btn');
            modalWishlistBtn.addEventListener('click', function() {
                const icon = this.querySelector('i');

                if (icon.classList.contains('far')) {
                    icon.classList.remove('far');
                    icon.classList.add('fas');
                    icon.style.color = '#e91e63';

                    // Show wishlist notification
                    showNotification('Added to wishlist!', '#e91e63');
                } else {
                    icon.classList.remove('fas');
                    icon.classList.add('far');
                    icon.style.color = '';

                    // Show wishlist removed notification
                    showNotification('Removed from wishlist', '#6c757d');
                }
            });
        });
    });

    // Notification helper function
    function showNotification(message, color) {
        const notification = document.createElement('div');
        notification.innerHTML = `<i class="fas fa-info-circle"></i> ${message}`;

        notification.style.position = 'fixed';
        notification.style.bottom = '20px';
        notification.style.right = '20px';
        notification.style.backgroundColor = color;
        notification.style.color = 'white';
        notification.style.padding = '10px 20px';
        notification.style.borderRadius = '5px';
        notification.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
        notification.style.zIndex = '1000';
        notification.style.display = 'flex';
        notification.style.alignItems = 'center';
        notification.style.gap = '10px';

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.opacity = '0';
            notification.style.transition = 'opacity 0.5s ease';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 500);
        }, 2000);
    }

    // Reset filters function
    window.resetFilters = function() {
        window.location.href = window.location.pathname;
    };
});