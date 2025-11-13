import React, { useState, useEffect } from 'react';
import './App.css';
import DataViewer from './DataViewer';

function App() {
  const [credentials, setCredentials] = useState({ username: 'admin', password: 'admin123' });
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [systemData, setSystemData] = useState(null);
  const [realJudgments, setRealJudgments] = useState([]);
  const [showDataViewer, setShowDataViewer] = useState(false);

  // جلب البيانات الحقيقية عند تسجيل الدخول
  const fetchRealData = async () => {
    try {
      // جلب الإحصائيات
      const statsResponse = await fetch('http://localhost:5000/api/stats');
      const stats = await statsResponse.json();
      setSystemData(stats);

      // جلب الأحكام الحقيقية
      const judgmentsResponse = await fetch('http://localhost:5000/api/judgments');
      const judgmentsData = await judgmentsResponse.json();
      
      if (judgmentsData.success) {
        setRealJudgments(judgmentsData.judgments);
      }
      
      console.log('📊 تم جلب البيانات:', { stats, judgments: judgmentsData });
    } catch (err) {
      console.error('خطأ في جلب البيانات الحقيقية:', err);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await fetch('http://localhost:5000/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      });

      const data = await response.json();

      if (response.ok) {
        setUser(data.user);
        localStorage.setItem('token', data.access_token);
        // جلب البيانات الحقيقية بعد تسجيل الدخول
        await fetchRealData();
      } else {
        setError(data.error || 'فشل في تسجيل الدخول');
      }
    } catch (err) {
      setError('تعذر الاتصال بالخادم. تأكد من تشغيل Backend على http://localhost:5000');
    }

    setLoading(false);
  };

  const handleLogout = () => {
    setUser(null);
    setSystemData(null);
    setRealJudgments([]);
    setShowDataViewer(false);
    localStorage.removeItem('token');
  };

  // تحديث البيانات كل 30 ثانية
  useEffect(() => {
    if (user && !showDataViewer) {
      const interval = setInterval(fetchRealData, 30000);
      return () => clearInterval(interval);
    }
  }, [user, showDataViewer]);

  // إذا كان عارض البيانات مفتوح
  if (showDataViewer) {
    return <DataViewer onBack={() => setShowDataViewer(false)} />;
  }

  if (user) {
    return (
      <div className="app" dir="rtl">
        <div className="container">
          <div className="logo">📊</div>
          <h1>مرحباً، {user.full_name}</h1>
          <p className="subtitle">لوحة التحكم الرئيسية</p>
          
          <div className="dashboard">
            {/* إحصائيات النظام */}
            <div className="stats">
              <div className="stat-card">
                <h3>🏛️ إجمالي الأحكام</h3>
                <p>{systemData?.total_judgments || 0}</p>
                <small>{systemData?.data_source || 'بيانات تجريبية'}</small>
              </div>
              <div className="stat-card">
                <h3>📊 الأعمدة المتاحة</h3>
                <p>{systemData?.headers?.length || 0}</p>
                <small>عمود في قاعدة البيانات</small>
              </div>
            </div>
            
            {/* معلومات البيانات المحملة */}
            {systemData && systemData.headers && systemData.headers.length > 0 && (
              <div className="data-info">
                <h3>📋 معلومات البيانات المحملة:</h3>
                <div className="headers-list">
                  <strong>أعمدة البيانات:</strong>
                  <ul>
                    {systemData.headers.slice(0, 8).map((header, index) => (
                      <li key={index}>{header}</li>
                    ))}
                    {systemData.headers.length > 8 && (
                      <li>... و {systemData.headers.length - 8} أعمدة أخرى</li>
                    )}
                  </ul>
                </div>
                
                <div style={{ marginTop: '15px' }}>
                  <button 
                    className="btn view-data-btn"
                    onClick={() => setShowDataViewer(true)}
                  >
                    🗄️ عرض جميع البيانات
                  </button>
                </div>
              </div>
            )}
            
            {/* عرض عينة من الأحكام الحقيقية */}
            {realJudgments && realJudgments.length > 0 && (
              <div className="judgments-preview">
                <h3>⚖️ عينة من الأحكام المحملة:</h3>
                <div className="judgments-list">
                  {realJudgments.slice(0, 3).map((judgment, index) => (
                    <div key={index} className="judgment-item">
                      <strong>الحكم #{index + 1}:</strong>
                      <div className="judgment-details">
                        {Object.keys(judgment).slice(0, 3).map(key => (
                          <p key={key}>
                            <strong>{key}:</strong> {
                              String(judgment[key]).length > 80 
                                ? String(judgment[key]).substring(0, 80) + '...'
                                : judgment[key]
                            }
                          </p>
                        ))}
                      </div>
                    </div>
                  ))}
                  
                  {realJudgments.length > 3 && (
                    <div className="more-judgments">
                      <p>و {realJudgments.length - 3} أحكام أخرى...</p>
                      <button 
                        className="btn view-all-btn"
                        onClick={() => setShowDataViewer(true)}
                      >
                        📋 عرض جميع الأحكام
                      </button>
                    </div>
                  )}
                </div>
              </div>
            )}
            
            {/* إذا لم تكن هناك بيانات حقيقية */}
            {(!realJudgments || realJudgments.length === 0) && (
              <div className="no-data-message">
                <h3>📁 لا توجد بيانات محملة</h3>
                <p>لتحميل البيانات الحقيقية:</p>
                <ol>
                  <li>اذهب إلى: <a href="http://localhost:5000/csv-reader" target="_blank" rel="noopener noreferrer">قارئ البيانات</a></li>
                  <li>ارفع ملف arabicljptraindata.csv</li>
                  <li>اضغط "🚀 تحديث Backend"</li>
                  <li>عد إلى هذه الصفحة أو اضغط "🔄 تحديث البيانات" أدناه</li>
                </ol>
                <button className="btn" onClick={fetchRealData}>
                  🔄 تحديث البيانات
                </button>
              </div>
            )}
            
            {/* الإجراءات السريعة */}
            <div className="actions">
              <h3>الإجراءات السريعة:</h3>
              <div className="action-grid">
                <button className="btn" onClick={() => window.open('http://localhost:5000/csv-reader', '_blank')}>
                  📁 تحميل بيانات جديدة
                </button>
                <button className="btn" onClick={fetchRealData}>
                  🔄 تحديث البيانات
                </button>
                {realJudgments.length > 0 && (
                  <button className="btn primary-btn" onClick={() => setShowDataViewer(true)}>
                    🗄️ عارض البيانات المتقدم
                  </button>
                )}
                <button className="btn" onClick={() => window.open('http://localhost:5000/api/stats', '_blank')}>
                  📊 إحصائيات JSON
                </button>
              </div>
            </div>
            
            {/* حالة النظام */}
            <div className="demo-info">
              <h3>حالة النظام:</h3>
              <p>✅ الخادم الخلفي متصل</p>
              <p>✅ المصادقة تعمل بنجاح</p>
              <p>👤 المستخدم: {user.username} ({user.role})</p>
              <p>📡 الخادم: http://localhost:5000</p>
              <p>🗄️ حالة البيانات: {systemData?.data_source || 'غير محددة'}</p>
              {systemData?.total_judgments > 0 && (
                <p>📊 البيانات المحملة: {systemData.total_judgments} حكم قانوني</p>
              )}
            </div>
          </div>
          
          <button className="btn logout-btn" onClick={handleLogout}>
            تسجيل الخروج
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="app" dir="rtl">
      <div className="container">
        <div className="logo">⚖️</div>
        <h1>نظام إدارة الأحكام القانونية</h1>
        <p className="subtitle">تسجيل الدخول إلى النظام</p>
        
        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label htmlFor="username">اسم المستخدم:</label>
            <input
              type="text"
              id="username"
              value={credentials.username}
              onChange={(e) => setCredentials({...credentials, username: e.target.value})}
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="password">كلمة المرور:</label>
            <input
              type="password"
              id="password"
              value={credentials.password}
              onChange={(e) => setCredentials({...credentials, password: e.target.value})}
              required
            />
          </div>
          
          <button type="submit" className="btn" disabled={loading}>
            {loading ? 'جاري تسجيل الدخول...' : 'تسجيل الدخول'}
          </button>
        </form>
        
        {error && <div className="error">{error}</div>}
        
        <div className="demo-info">
          <h3>بيانات تجريبية:</h3>
          <p><strong>اسم المستخدم:</strong> admin</p>
          <p><strong>كلمة المرور:</strong> admin123</p>
          <hr />
          <p><strong>رفع البيانات:</strong> <a href="http://localhost:5000/csv-reader" target="_blank" rel="noopener noreferrer">اضغط هنا</a></p>
        </div>
      </div>
    </div>
  );
}

export default App;
