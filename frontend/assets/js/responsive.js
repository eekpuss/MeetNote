/**
 * MeetNote Responsive JavaScript
 * Fungsi-fungsi untuk menangani responsifitas halaman
 */

// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    // Handler untuk perubahan ukuran layar
    handleWindowResize();
    
    // Event listener untuk resize window
    window.addEventListener('resize', handleWindowResize);
    
    // Inisialisasi tabel responsif
    initResponsiveTables();
    
    // Inisialisasi collapse pada card
    initCardCollapse();
    
    // Handle orientasi pada perangkat mobile
    handleOrientation();
});

/**
 * Fungsi untuk menangani perubahan ukuran layar
 */
function handleWindowResize() {
    const windowWidth = window.innerWidth;
    
    // Mengatur sidebar secara otomatis
    if (windowWidth < 768) {
        // Mobile view - collapse sidebar
        const sidebar = document.getElementById('sidebar');
        if (sidebar && !sidebar.classList.contains('collapsed') && !sidebar.classList.contains('mobile-visible')) {
            sidebar.classList.add('collapsed');
            
            const mainContent = document.getElementById('mainContent');
            if (mainContent) {
                mainContent.classList.add('expanded');
            }
        }
    }
    
    // Mengatur tabel yang responsif
    const tables = document.querySelectorAll('table.table');
    tables.forEach(table => {
        const parentDiv = table.parentNode;
        if (!parentDiv.classList.contains('table-responsive') && windowWidth < 992) {
            // Bungkus tabel dengan div.table-responsive jika belum
            if (parentDiv.nodeName !== 'DIV' || !parentDiv.classList.contains('table-responsive')) {
                const wrapper = document.createElement('div');
                wrapper.className = 'table-responsive';
                table.parentNode.insertBefore(wrapper, table);
                wrapper.appendChild(table);
            }
        }
    });
    
    // Menyesuaikan form layout
    adjustFormLayout(windowWidth);
    
    // Menyesuaikan card layout
    adjustCardLayout(windowWidth);
}

/**
 * Inisialisasi tabel responsif
 */
function initResponsiveTables() {
    const tables = document.querySelectorAll('table.table');
    
    tables.forEach(table => {
        // Tambahkan atribut data-label pada setiap sel berdasarkan header-nya
        const headers = Array.from(table.querySelectorAll('thead th')).map(th => th.textContent.trim());
        
        table.querySelectorAll('tbody tr').forEach(row => {
            Array.from(row.querySelectorAll('td')).forEach((cell, index) => {
                if (headers[index]) {
                    cell.setAttribute('data-label', headers[index]);
                }
            });
        });
    });
}

/**
 * Inisialisasi collapse pada card
 */
function initCardCollapse() {
    const cardHeaders = document.querySelectorAll('.card-header[data-bs-toggle="collapse"]');
    
    cardHeaders.forEach(header => {
        header.addEventListener('click', function() {
            const target = document.querySelector(this.getAttribute('data-bs-target'));
            if (target) {
                target.classList.toggle('show');
                
                // Toggle ikon jika ada
                const icon = this.querySelector('.collapse-icon');
                if (icon) {
                    if (target.classList.contains('show')) {
                        icon.classList.remove('fa-chevron-down');
                        icon.classList.add('fa-chevron-up');
                    } else {
                        icon.classList.remove('fa-chevron-up');
                        icon.classList.add('fa-chevron-down');
                    }
                }
            }
        });
    });
}

/**
 * Handle orientasi pada perangkat mobile
 */
function handleOrientation() {
    // Deteksi perubahan orientasi
    window.addEventListener('orientationchange', function() {
        // Re-atur layout setelah orientasi berubah
        setTimeout(handleWindowResize, 300);
    });
}

/**
 * Menyesuaikan layout form berdasarkan ukuran layar
 */
function adjustFormLayout(windowWidth) {
    if (windowWidth < 768) {
        // Pada layar kecil, buat form field full width
        document.querySelectorAll('.row .col-md-6, .row .col-md-4, .row .col-md-3').forEach(col => {
            col.style.marginBottom = '15px';
        });
    } else {
        // Reset pada layar lebih besar
        document.querySelectorAll('.row .col-md-6, .row .col-md-4, .row .col-md-3').forEach(col => {
            col.style.marginBottom = '';
        });
    }
}

/**
 * Menyesuaikan layout card berdasarkan ukuran layar
 */
function adjustCardLayout(windowWidth) {
    // Menyesuaikan padding pada card di layar kecil
    if (windowWidth < 576) {
        document.querySelectorAll('.card-body').forEach(cardBody => {
            cardBody.style.padding = '15px';
        });
        
        document.querySelectorAll('.card-header').forEach(cardHeader => {
            cardHeader.style.padding = '15px';
        });
    } else {
        // Reset pada layar lebih besar
        document.querySelectorAll('.card-body').forEach(cardBody => {
            cardBody.style.padding = '';
        });
        
        document.querySelectorAll('.card-header').forEach(cardHeader => {
            cardHeader.style.padding = '';
        });
    }
}

/**
 * Membuat tabel responsif pada perangkat mobile
 * Saat viewport < 768px, tabel akan menjadi cards
 */
function makeTableResponsive(tableId) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    // Deteksi ukuran layar
    const windowWidth = window.innerWidth;
    
    // Jika mobile view (<768px)
    if (windowWidth < 768) {
        // Dapatkan semua header
        const headers = Array.from(table.querySelectorAll('thead th')).map(th => th.textContent.trim());
        
        // Ambil tbody untuk manipulasi
        const tbody = table.querySelector('tbody');
        
        // Simpan HTML original
        if (!table.getAttribute('data-original')) {
            table.setAttribute('data-original', tbody.innerHTML);
        }
        
        // Tambahkan class
        table.classList.add('table-to-cards');
        
        // Ubah tabel menjadi cards
        const rows = tbody.querySelectorAll('tr');
        
        // Buat card untuk setiap row
        const cards = [];
        
        rows.forEach(row => {
            const cells = row.querySelectorAll('td');
            
            // Buat card
            const card = document.createElement('div');
            card.className = 'card mb-3';
            
            // Buat card body
            const cardBody = document.createElement('div');
            cardBody.className = 'card-body p-3';
            
            // Isi card body dengan data
            cells.forEach((cell, index) => {
                if (headers[index]) {
                    const item = document.createElement('div');
                    item.className = 'card-item mb-2';
                    
                    const label = document.createElement('div');
                    label.className = 'card-item-label';
                    label.textContent = headers[index];
                    
                    const value = document.createElement('div');
                    value.className = 'card-item-value';
                    value.innerHTML = cell.innerHTML;
                    
                    item.appendChild(label);
                    item.appendChild(value);
                    cardBody.appendChild(item);
                }
            });
            
            card.appendChild(cardBody);
            cards.push(card);
        });
        
        // Ganti tbody dengan cards
        tbody.innerHTML = '';
        const cardContainer = document.createElement('div');
        cardContainer.className = 'card-container';
        
        cards.forEach(card => {
            cardContainer.appendChild(card);
        });
        
        tbody.appendChild(cardContainer);
    } else {
        // Kembalikan ke tampilan tabel normal jika layar > 768px
        if (table.getAttribute('data-original')) {
            const tbody = table.querySelector('tbody');
            tbody.innerHTML = table.getAttribute('data-original');
            table.classList.remove('table-to-cards');
        }
    }
}

/**
 * Deteksi perangkat untuk menyesuaikan UI
 */
function detectDevice() {
    const userAgent = navigator.userAgent.toLowerCase();
    let deviceType = 'desktop';
    
    // Deteksi perangkat
    if (/android|webos|iphone|ipad|ipod|blackberry|iemobile|opera mini/i.test(userAgent)) {
        deviceType = 'mobile';
        
        if (/ipad/i.test(userAgent) || (userAgent.includes('macintosh') && 'ontouchend' in document)) {
            deviceType = 'tablet';
        }
    }
    
    // Set class pada body
    document.body.classList.add(`device-${deviceType}`);
    
    return deviceType;
}

// Panggil fungsi deteksi perangkat saat page load
document.addEventListener('DOMContentLoaded', detectDevice);