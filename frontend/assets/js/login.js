// assets/js/login.js
document.addEventListener('DOMContentLoaded', function() {
    // Cek apakah pengguna sudah login (token ada di localStorage)
    const token = localStorage.getItem('token');
    if (token) {
        // Jika sudah login, redirect ke dashboard
        window.location.replace('index.html');
        return;
    }

    // Toggle password visibility
    const togglePassword = document.querySelector('.toggle-password');
    const passwordInput = document.querySelector('#password');
    
    if (togglePassword && passwordInput) {
        togglePassword.addEventListener('click', function() {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            
            // Toggle icon
            this.querySelector('i').classList.toggle('fa-eye');
            this.querySelector('i').classList.toggle('fa-eye-slash');
        });
    }
    
    // Handle login form submission
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            // Validasi sederhana
            if (!email || !password) {
                showToast('Email dan password harus diisi', 'danger');
                return;
            }
            
            // Tampilkan loading
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Memproses...';
            
            // Coba login ke API
            fetch('http://localhost:5000/api/auth/login', {
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
                
                // Tampilkan pesan sukses
                showToast('Login berhasil! Mengalihkan ke dashboard...', 'success');
                
                // Gunakan hard redirect
                window.location.replace('index.html');
            })
            .catch(error => {
                console.error('Login error:', error);
                
                // Jika API tidak bisa diakses, coba dengan kredensial demo
                if (email === 'admin@meetnote.com' && password === 'admin123') {
                    // Simpan token dummy
                    localStorage.setItem('token', 'dummy-token');
                    localStorage.setItem('user', JSON.stringify({
                        id: 1,
                        username: 'Admin',
                        email: 'admin@meetnote.com',
                        is_admin: true
                    }));
                    
                    // Tampilkan pesan sukses
                    showToast('Login berhasil dengan akun demo! Mengalihkan ke dashboard...', 'success');
                    
                    // Gunakan hard redirect
                    window.location.replace('index.html');
                } else if (email === 'user@meetnote.com' && password === 'user123') {
                    // Simpan token dummy
                    localStorage.setItem('token', 'dummy-token');
                    localStorage.setItem('user', JSON.stringify({
                        id: 2,
                        username: 'User',
                        email: 'user@meetnote.com',
                        is_admin: false
                    }));
                    
                    // Tampilkan pesan sukses
                    showToast('Login berhasil dengan akun demo! Mengalihkan ke dashboard...', 'success');
                    
                    // Gunakan hard redirect
                    window.location.replace('index.html');
                } else {
                    showToast('Email atau password salah', 'danger');
                    
                    // Reset button
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }
            });
        });
    }
    
    // Fungsi untuk menampilkan toast
    function showToast(message, type = 'success') {
        // Cek apakah toast container sudah ada
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
});