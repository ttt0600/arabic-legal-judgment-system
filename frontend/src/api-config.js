// تحديث رابط API حسب المنفذ المستخدم
const API_BASE_URL = 'http://localhost:5001'; // غير هذا إذا كان المنفذ مختلف

// تحديث جميع طلبات fetch في Frontend
function updateApiUrl() {
    // تحديث جميع استدعاءات fetch
    const originalFetch = window.fetch;
    window.fetch = function(url, options) {
        if (url.startsWith('http://localhost:5000')) {
            url = url.replace('http://localhost:5000', API_BASE_URL);
        }
        return originalFetch.call(this, url, options);
    };
}

// تشغيل التحديث عند تحميل الصفحة
updateApiUrl();

console.log(`✅ تم تحديث API URL إلى: ${API_BASE_URL}`);
