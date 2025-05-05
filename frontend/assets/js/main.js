/**
 * MeetNote - Main JavaScript File
 * Berisi fungsi-fungsi umum yang digunakan di seluruh aplikasi
 */

// Variabel global
const API_URL = 'http://localhost:5000/api';

// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    // Inisialisasi sidebar toggle
    initSidebar();
    
    // Cek autentikasi
    checkAuthentication();
    
    // Setup logout handler
    setupLogout();
    
    // Muat komponen
    loadComponents();
});

/**
 * Inisialisasi toggle sidebar
 */
function initSidebar() {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('mainContent');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const mobileToggle = document.getElementById('mobileToggle');
    
    // Desktop sidebar toggle
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('collapsed');
            mainContent.classList.toggle('expanded');
            
            // Simpan status sidebar ke localStorage
            localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));
        });
    }
    
    // Mobile sidebar toggle
    if (mobileToggle) {
        mobileToggle.addEventListener('click', function() {
            sidebar.classList.toggle('mobile-visible');
            
            // Tambahkan overlay pada mobile
            if (sidebar.classList.contains('mobile-visible')) {
                const overlay = document.createElement('div');
                overlay.className = 'sidebar-overlay';
                overlay.addEventListener('click', function() {
                    sidebar.classList.remove('mobile-visible');
                    this.remove();
                });
                document.body.appendChild(overlay);
            } else {
                const overlay = document.querySelector('.sidebar-overlay');
                if (overlay) overlay.remove();
            }
        });
    }
    
    // Restore sidebar state dari localStorage
    const sidebarCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
    if (sidebarCollapsed && sidebar) {
        sidebar.classList.add('collapsed');
        if (mainContent) mainContent.classList.add('expanded');
    }
    
    // Close sidebar on small screens when clicking menu items
    const menuItems = document.querySelectorAll('.sidebar .menu-item');
    if (window.innerWidth <= 768) {
        menuItems.forEach(item => {
            item.addEventListener('click', function() {
                if (sidebar) sidebar.classList.remove('mobile-visible');
                const overlay = document.querySelector('.sidebar-overlay');
                if (overlay) overlay.remove();
            });
        });
    }
}

/**
 * Cek status autentikasi pengguna
 */
function checkAuthentication() {
    // Skip untuk halaman login
    if (window.location.pathname.includes('login.html')) {
        return;
    }
    
    const token = localStorage.getItem('token');
    
    if (!token) {
        // Redirect ke halaman login jika tidak ada token
        window.location.href = getBasePath() + 'login.html';
        return;
    }
    
    // Verifikasi token dengan request ke API
    fetch(API_URL + '/auth/me', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Invalid token');
        }
        return response.json();
    })
    .then(user => {
        // Simpan info user ke localStorage
        localStorage.setItem('user', JSON.stringify(user));
        
        // Update UI dengan info user
        updateUserInfo(user);
    })
    .catch(error => {
        console.error('Authentication error:', error);
        
        // Hapus token dan redirect ke login
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = getBasePath() + 'login.html';
    });
}

/**
 * Update UI dengan informasi pengguna
 */
function updateUserInfo(user) {
    // Update avatar dengan inisial
    const userAvatarElements = document.querySelectorAll('.user-avatar');
    const initials = getInitials(user.username);
    
    userAvatarElements.forEach(element => {
        element.textContent = initials;
    });
    
    // Update nama dan role
    const userNameElements = document.querySelectorAll('.user-name');
    const userRoleElements = document.querySelectorAll('.user-role');
    
    userNameElements.forEach(element => {
        element.textContent = user.username;
    });
    
    userRoleElements.forEach(element => {
        element.textContent = user.is_admin ? 'Administrator' : 'User';
    });
}

/**
 * Mendapatkan inisial dari nama
 */
function getInitials(name) {
    if (!name) return '';
    
    const parts = name.split(' ');
    if (parts.length === 1) {
        return parts[0].substring(0, 2).toUpperCase();
    }
    
    return (parts[0].charAt(0) + parts[1].charAt(0)).toUpperCase();
}

/**
 * Setup handler untuk logout
 */
function setupLogout() {
    const logoutButtons = document.querySelectorAll('.fa-sign-out-alt').forEach(element => {
        element.parentElement.addEventListener('click', function(event) {
            event.preventDefault();
            logout();
        });
    });
}

/**
 * Logout user
 */
function logout() {
    // Hapus token dan info user
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    
    // Redirect ke halaman login
    window.location.href = getBasePath() + 'login.html';
}

/**
 * Mendapatkan token dari localStorage
 */
function getToken() {
    return localStorage.getItem('token');
}

/**
 * Mendapatkan base path untuk URL
 */
function getBasePath() {
    const path = window.location.pathname;
    
    if (path.includes('/pages/')) {
        return '../../';
    } else if (path.includes('/index.html') || path === '/') {
        return './';
    } else {
        return '../';
    }
}

/**
 * Format tanggal
 */
function formatDate(dateString, format = 'long') {
    if (!dateString) return '-';
    
    const date = new Date(dateString);
    
    if (format === 'long') {
        return date.toLocaleDateString('id-ID', {
            day: 'numeric',
            month: 'long',
            year: 'numeric'
        });
    } else if (format === 'short') {
        return date.toLocaleDateString('id-ID');
    } else if (format === 'time') {
        return date.toLocaleTimeString('id-ID', {
            hour: '2-digit',
            minute: '2-digit'
        });
    } else if (format === 'datetime') {
        return date.toLocaleString('id-ID');
    } else if (format === 'relative') {
        return getRelativeTime(date);
    }
    
    return date.toLocaleDateString('id-ID');
}

/**
 * Mendapatkan waktu relatif (contoh: "5 menit yang lalu")
 */
function getRelativeTime(date) {
    const now = new Date();
    const diffMs = now - date;
    const diffSeconds = Math.floor(diffMs / 1000);
    const diffMinutes = Math.floor(diffSeconds / 60);
    const diffHours = Math.floor(diffMinutes / 60);
    const diffDays = Math.floor(diffHours / 24);
    
    if (diffSeconds < 60) {
        return 'Baru saja';
    } else if (diffMinutes < 60) {
        return `${diffMinutes} menit yang lalu`;
    } else if (diffHours < 24) {
        return `${diffHours} jam yang lalu`;
    } else if (diffDays < 7) {
        return `${diffDays} hari yang lalu`;
    } else {
        return formatDate(date);
    }
}

/**
 * Menampilkan notifikasi toast
 */
function showToast(message, type = 'success') {
    // Cek apakah container toast sudah ada
    let toastContainer = document.querySelector('.toast-container');
    
    if (!toastContainer) {
        // Buat container toast jika belum ada
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(toastContainer);
    }
    
    // Buat toast element
    const toastEl = document.createElement('div');
    toastEl.className = `toast align-items-center text-white bg-${type} border-0`;
    toastEl.setAttribute('role', 'alert');
    toastEl.setAttribute('aria-live', 'assertive');
    toastEl.setAttribute('aria-atomic', 'true');
    
    // Buat toast content
    toastEl.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    
    // Tambahkan toast ke container
    toastContainer.appendChild(toastEl);
    
    // Inisialisasi toast dengan Bootstrap
    const toast = new bootstrap.Toast(toastEl, { delay: 3000 });
    
    // Tampilkan toast
    toast.show();
    
    // Hapus toast dari DOM setelah disembunyikan
    toastEl.addEventListener('hidden.bs.toast', function() {
        this.remove();
    });
}

/**
 * Membuat elemen loading spinner
 */
function createLoadingSpinner() {
    const spinner = document.createElement('div');
    spinner.className = 'spinner-border spinner-border-sm text-primary';
    spinner.setAttribute('role', 'status');
    spinner.innerHTML = '<span class="visually-hidden">Loading...</span>';
    return spinner;
}

/**
 * Memuat komponen HTML
 * @param {string} elementId - ID elemen tempat komponen akan ditempatkan
 * @param {string} componentPath - Path relatif ke komponen
 * @returns {Promise} - Promise yang terpenuhi ketika komponen dimuat
 */
async function loadComponent(elementId, componentPath) {
    try {
        const response = await fetch(componentPath);
        const html = await response.text();
        const element = document.getElementById(elementId);
        
        if (element) {
            element.innerHTML = html;
            
            // Execute scripts dari komponen
            const scriptElements = element.querySelectorAll('script');
            scriptElements.forEach(script => {
                const newScript = document.createElement('script');
                Array.from(script.attributes).forEach(attr => {
                    newScript.setAttribute(attr.name, attr.value);
                });
                newScript.innerHTML = script.innerHTML;
                script.parentNode.replaceChild(newScript, script);
            });
            
            return true;
        }
        
        return false;
    } catch (error) {
        console.error(`Error loading component ${componentPath}:`, error);
        return false;
    }
}

/**
 * Memuat semua komponen utama
 * @param {string} basePath - Path dasar ke direktori components
 */
function loadComponents(basePath) {
    // Tentukan path komponen berdasarkan lokasi halaman saat ini
    let componentsPath = './components/';
    
    // Jika berada di subfolder, sesuaikan path
    const path = window.location.pathname;
    
    if (path.includes('/pages/')) {
        // Jika berada di /pages/
        componentsPath = '../components/';
        
        // Jika berada di /pages/meetings/ atau /pages/todos/
        if (path.includes('/meetings/') || path.includes('/todos/')) {
            componentsPath = '../../components/';
        }
    }
    
    // Override jika basePath diberikan
    if (basePath) {
        componentsPath = basePath;
    }
    
    // Muat komponen utama
    const containers = {
        'sidebar-container': 'sidebar.html',
        'header-container': 'header.html',
        'toast-container': 'toast.html',
        'modal-container': 'modal.html',
        'loading-container': 'loading.html',
        'breadcrumb-container': 'breadcrumb.html',
        'footer-container': 'footer.html'
    };
    
    // Muat komponen jika containernya ada
    Object.entries(containers).forEach(([containerId, filename]) => {
        if (document.getElementById(containerId)) {
            loadComponent(containerId, componentsPath + filename);
        }
    });
}

/**
 * Menghandle error dari API
 */
function handleApiError(error) {
    console.error('API Error:', error);
    
    let errorMessage = 'Terjadi kesalahan. Silakan coba lagi.';
    
    if (error.response) {
        // Server merespons dengan status code diluar range 2xx
        const status = error.response.status;
        
        if (status === 401) {
            errorMessage = 'Sesi telah berakhir. Silakan login kembali.';
            logout();
        } else if (status === 403) {
            errorMessage = 'Anda tidak memiliki izin untuk melakukan tindakan ini.';
        } else if (status === 404) {
            errorMessage = 'Data tidak ditemukan.';
        } else if (status === 422) {
            errorMessage = 'Data yang dimasukkan tidak valid.';
        } else if (status >= 500) {
            errorMessage = 'Terjadi kesalahan pada server. Silakan coba lagi nanti.';
        }
    } else if (error.request) {
        // Request dibuat tapi tidak ada respons
        errorMessage = 'Tidak dapat terhubung ke server. Periksa koneksi internet Anda.';
    }
    
    showToast(errorMessage, 'danger');
}

/**
 * Menghandle login form
 */
function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    // Validasi input
    if (!email || !password) {
        showToast('Email dan password harus diisi', 'danger');
        return;
    }
    
    // Disable form saat proses login
    const submitButton = document.querySelector('button[type="submit"]');
    const originalText = submitButton.textContent;
    submitButton.disabled = true;
    submitButton.innerHTML = '';
    submitButton.appendChild(createLoadingSpinner());
    submitButton.append(' Logging in...');
    
    // Kirim request login ke API
    fetch(API_URL + '/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Login failed');
        }
        return response.json();
    })
    .then(data => {
        // Simpan token dan user info
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('user', JSON.stringify(data.user));
        
        // Redirect ke dashboard
        window.location.href = 'index.html';
    })
    .catch(error => {
        console.error('Login error:', error);
        showToast('Email atau password salah', 'danger');
        
        // Reset form
        submitButton.disabled = false;
        submitButton.textContent = originalText;
    });
}

/**
 * Menghandle form submit yang membutuhkan konfirmasi
 */
function handleConfirmSubmit(event, confirmMessage, callback) {
    event.preventDefault();
    
    if (confirm(confirmMessage)) {
        callback(event.target);
    }
}

/**
 * Mendapatkan status dari todo
 */
function getTodoStatusBadge(status) {
    let badgeClass, statusText;
    
    switch (status) {
        case 'not_started':
            badgeClass = 'bg-danger';
            statusText = 'Belum Dimulai';
            break;
        case 'in_progress':
            badgeClass = 'bg-warning';
            statusText = 'Sedang Dikerjakan';
            break;
        case 'completed':
            badgeClass = 'bg-success';
            statusText = 'Selesai';
            break;
        default:
            badgeClass = 'bg-secondary';
            statusText = 'Tidak Diketahui';
    }
    
    return `<span class="badge ${badgeClass}">${statusText}</span>`;
}

/**
 * Mendapatkan prioritas dari todo
 */
function getTodoPriorityBadge(priority) {
    let badgeClass, priorityText;
    
    switch (priority) {
        case 'low':
            badgeClass = 'bg-info';
            priorityText = 'Rendah';
            break;
        case 'medium':
            badgeClass = 'bg-warning';
            priorityText = 'Sedang';
            break;
        case 'high':
            badgeClass = 'bg-danger';
            priorityText = 'Tinggi';
            break;
        default:
            badgeClass = 'bg-secondary';
            priorityText = 'Tidak Diketahui';
    }
    
    return `<span class="badge ${badgeClass}">${priorityText}</span>`;
}

/**
 * Menampilkan dialog konfirmasi
 */
function showConfirmDialog(message, callback) {
    // Buat dialog element
    const modalId = 'confirmDialog';
    let modalEl = document.getElementById(modalId);
    
    if (!modalEl) {
        modalEl = document.createElement('div');
        modalEl.className = 'modal fade';
        modalEl.id = modalId;
        modalEl.setAttribute('tabindex', '-1');
        modalEl.setAttribute('aria-hidden', 'true');
        
        modalEl.innerHTML = `
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Konfirmasi</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <p id="confirmMessage"></p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Batal</button>
                        <button type="button" class="btn btn-primary" id="confirmButton">Ya</button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modalEl);
    }
    
    // Set message
    document.getElementById('confirmMessage').textContent = message;
    
    // Inisialisasi modal dengan Bootstrap
    const modal = new bootstrap.Modal(modalEl);
    
    // Tambahkan event listener ke tombol konfirmasi
    document.getElementById('confirmButton').onclick = function() {
        modal.hide();
        callback();
    };
    
    // Tampilkan modal
    modal.show();
}

/**
 * Export tabel ke CSV
 */
function exportTableToCSV(tableId, filename = 'data.csv') {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    // Ambil header
    const headers = [];
    const headerCells = table.querySelectorAll('thead th');
    
    headerCells.forEach(cell => {
        headers.push(cell.textContent.trim());
    });
    
    // Ambil data
    const rows = [];
    const rowCells = table.querySelectorAll('tbody tr');
    
    rowCells.forEach(row => {
        const rowData = [];
        const cells = row.querySelectorAll('td');
        
        cells.forEach(cell => {
            // Hilangkan HTML tags dan gunakan hanya text
            const div = document.createElement('div');
            div.innerHTML = cell.innerHTML;
            rowData.push(div.textContent.trim());
        });
        
        rows.push(rowData);
    });
    
    // Gabungkan header dan data
    const csvContent = [
        headers.join(','),
        ...rows.map(row => row.join(','))
    ].join('\n');
    
    // Buat link download
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    
    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    link.style.display = 'none';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

/**
 * Fungsi untuk debounce (membatasi frekuensi eksekusi fungsi)
 */
function debounce(func, delay) {
    let timeoutId;
    
    return function(...args) {
        const context = this;
        
        clearTimeout(timeoutId);
        
        timeoutId = setTimeout(() => {
            func.apply(context, args);
        }, delay);
    };
}