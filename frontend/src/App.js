import React, { useState, useEffect, useContext, createContext } from 'react';
import { Search, FileText, Gavel, Building, Users, BarChart3, Settings, Menu, Bell, User, LogOut, Plus, Eye, Edit, Trash2, Download, Calendar, Filter, ChevronDown, ChevronRight, AlertCircle, CheckCircle, Clock, Scale, BookOpen, Upload, X } from 'lucide-react';

// Auth Context
const AuthContext = createContext();

const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(localStorage.getItem('token'));

  useEffect(() => {
    if (token) {
      fetchUser();
    } else {
      setLoading(false);
    }
  }, [token]);

  const fetchUser = async () => {
    try {
      const response = await fetch('/api/auth/me', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setUser(data.data.user);
      } else {
        logout();
      }
    } catch (error) {
      console.error('Error fetching user:', error);
      logout();
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, password) => {
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
      });

      const data = await response.json();
      
      if (data.success) {
        setToken(data.data.token);
        setUser(data.data.user);
        localStorage.setItem('token', data.data.token);
        return { success: true };
      } else {
        return { success: false, message: data.message };
      }
    } catch (error) {
      return { success: false, message: 'خطأ في الاتصال بالخادم' };
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('token');
  };

  const value = {
    user,
    login,
    logout,
    loading,
    token
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// API Service
const apiService = {
  baseURL: '/api',
  
  async request(endpoint, options = {}) {
    const token = localStorage.getItem('token');
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` })
      },
      ...options
    };

    try {
      const response = await fetch(`${this.baseURL}${endpoint}`, config);
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.message || 'حدث خطأ');
      }
      
      return data;
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }
};

// Cases List Component
const CasesList = () => {
  const [cases, setCases] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    fetchCases();
  }, []);

  const fetchCases = async () => {
    try {
      const response = await apiService.request('/cases');
      setCases(response.data || []);
    } catch (error) {
      console.error('Error fetching cases:', error);
      setCases([
        {
          _id: '1',
          caseNumber: '2024/001',
          title: 'دعوى مدنية - نزاع تجاري',
          status: 'under_review',
          type: 'civil',
          dates: { filed: new Date() },
          court: { name: 'المحكمة العامة بالرياض' },
          judge: { name: 'القاضي أحمد محمد' }
        },
        {
          _id: '2', 
          caseNumber: '2024/002',
          title: 'دعوى عمالية - مستحقات موظف',
          status: 'scheduled',
          type: 'labor',
          dates: { filed: new Date() },
          court: { name: 'محكمة العمل بالرياض' },
          judge: { name: 'القاضية فاطمة علي' }
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const statusLabels = {
    registered: 'مسجلة',
    under_review: 'قيد المراجعة',
    scheduled: 'محددة موعد',
    decided: 'صدر حكم'
  };

  const statusColors = {
    registered: 'bg-blue-100 text-blue-800',
    under_review: 'bg-yellow-100 text-yellow-800',
    scheduled: 'bg-purple-100 text-purple-800',
    decided: 'bg-green-100 text-green-800'
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">القضايا</h1>
        <button className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700">
          <Plus className="h-4 w-4 ml-2" />
          قضية جديدة
        </button>
      </div>

      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        {cases.length > 0 ? (
          <ul className="divide-y divide-gray-200">
            {cases.map((case_) => (
              <li key={case_._id} className="px-6 py-4 hover:bg-gray-50">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        <p className="text-lg font-medium text-blue-600 truncate">
                          {case_.caseNumber}
                        </p>
                        <span className={`mr-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${statusColors[case_.status] || 'bg-gray-100 text-gray-800'}`}>
                          {statusLabels[case_.status] || case_.status}
                        </span>
                      </div>
                      <div className="flex items-center space-x-2 space-x-reverse">
                        <button className="text-gray-400 hover:text-gray-500">
                          <Eye className="h-5 w-5" />
                        </button>
                        <button className="text-gray-400 hover:text-gray-500">
                          <Edit className="h-5 w-5" />
                        </button>
                      </div>
                    </div>
                    <p className="mt-1 text-sm text-gray-900">{case_.title}</p>
                    <div className="mt-2 flex items-center text-sm text-gray-500 space-x-4 space-x-reverse">
                      <div className="flex items-center">
                        <Building className="flex-shrink-0 ml-1.5 h-4 w-4 text-gray-400" />
                        {case_.court?.name}
                      </div>
                      <div className="flex items-center">
                        <Calendar className="flex-shrink-0 ml-1.5 h-4 w-4 text-gray-400" />
                        {new Date(case_.dates?.filed).toLocaleDateString('ar-SA')}
                      </div>
                      {case_.judge && (
                        <div className="flex items-center">
                          <User className="flex-shrink-0 ml-1.5 h-4 w-4 text-gray-400" />
                          {case_.judge.name}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <div className="text-center py-12">
            <FileText className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">لا توجد قضايا</h3>
            <p className="mt-1 text-sm text-gray-500">ابدأ بإنشاء قضية جديدة</p>
          </div>
        )}
      </div>
    </div>
  );
};

// Login Component  
const LoginPage = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    const result = await login(formData.email, formData.password);
    
    if (!result.success) {
      setError(result.message);
    }
    
    setLoading(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <div className="mx-auto h-12 w-12 flex items-center justify-center bg-blue-600 rounded-full">
            <Scale className="h-8 w-8 text-white" />
          </div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            تسجيل الدخول
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            نظام الأحكام القضائية
          </p>
        </div>
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <div className="rounded-md bg-red-50 p-4">
              <div className="flex">
                <div className="flex-shrink-0">
                  <AlertCircle className="h-5 w-5 text-red-400" />
                </div>
                <div className="mr-3">
                  <div className="text-sm text-red-700">{error}</div>
                </div>
              </div>
            </div>
          )}
          
          <div className="space-y-4">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                البريد الإلكتروني
              </label>
              <input
                id="email"
                name="email"
                type="email"
                required
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
                className="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                placeholder="admin@court.gov.sa"
              />
            </div>
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                كلمة المرور
              </label>
              <input
                id="password"
                name="password"
                type="password"
                required
                value={formData.password}
                onChange={(e) => setFormData({...formData, password: e.target.value})}
                className="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                placeholder="كلمة المرور"
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={loading}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
            >
              {loading ? (
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              ) : (
                'تسجيل الدخول'
              )}
            </button>
          </div>
        </form>
        
        <div className="text-center">
          <p className="text-sm text-gray-600">
            للاختبار:<br />
            البريد الإلكتروني: admin@court.gov.sa<br />
            كلمة المرور: Admin123!
          </p>
        </div>
      </div>
    </div>
  );
};

// Dashboard Component
const Dashboard = () => {
  const [stats, setStats] = useState({
    totalCases: 125,
    totalJudgments: 89,
    totalDocuments: 342,
    recentCases: 12
  });

  const statCards = [
    {
      title: 'إجمالي القضايا',
      value: stats.totalCases,
      icon: FileText,
      color: 'bg-blue-500',
      change: '+12%'
    },
    {
      title: 'الأحكام الصادرة',
      value: stats.totalJudgments,
      icon: Gavel,
      color: 'bg-green-500',
      change: '+8%'
    },
    {
      title: 'الوثائق',
      value: stats.totalDocuments,
      icon: BookOpen,
      color: 'bg-yellow-500',
      change: '+5%'
    },
    {
      title: 'القضايا الحديثة',
      value: stats.recentCases,
      icon: Clock,
      color: 'bg-purple-500',
      change: '+15%'
    }
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">لوحة التحكم</h1>
        <div className="text-sm text-gray-500">
          آخر تحديث: {new Date().toLocaleString('ar-SA')}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat, index) => (
          <div key={index} className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className={`inline-flex items-center justify-center p-3 ${stat.color} rounded-md`}>
                    <stat.icon className="h-6 w-6 text-white" />
                  </div>
                </div>
                <div className="mr-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">{stat.title}</dt>
                    <dd className="flex items-baseline">
                      <div className="text-2xl font-semibold text-gray-900">{stat.value.toLocaleString()}</div>
                      <div className="mr-2 flex items-baseline text-sm font-semibold text-green-600">
                        {stat.change}
                      </div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">القضايا الحديثة</h3>
            <div className="flow-root">
              <ul className="-mb-8">
                {[1, 2, 3].map((item, index) => (
                  <li key={index}>
                    <div className="relative pb-8">
                      {index !== 2 && (
                        <span className="absolute top-4 right-4 -mr-px h-full w-0.5 bg-gray-200" />
                      )}
                      <div className="relative flex space-x-3 space-x-reverse">
                        <div>
                          <span className="h-8 w-8 rounded-full bg-blue-500 flex items-center justify-center ring-8 ring-white">
                            <FileText className="h-4 w-4 text-white" />
                          </span>
                        </div>
                        <div className="min-w-0 flex-1 pt-1.5 flex justify-between space-x-4 space-x-reverse">
                          <div>
                            <p className="text-sm text-gray-500">
                              قضية جديدة{' '}
                              <span className="font-medium text-gray-900">دعوى مدنية رقم {2024000 + index}</span>
                            </p>
                          </div>
                          <div className="text-left text-sm whitespace-nowrap text-gray-500">
                            <time>منذ {index + 1} ساعة</time>
                          </div>
                        </div>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">الأحكام الأخيرة</h3>
            <div className="flow-root">
              <ul className="-mb-8">
                {[1, 2, 3].map((item, index) => (
                  <li key={index}>
                    <div className="relative pb-8">
                      {index !== 2 && (
                        <span className="absolute top-4 right-4 -mr-px h-full w-0.5 bg-gray-200" />
                      )}
                      <div className="relative flex space-x-3 space-x-reverse">
                        <div>
                          <span className="h-8 w-8 rounded-full bg-green-500 flex items-center justify-center ring-8 ring-white">
                            <Gavel className="h-4 w-4 text-white" />
                          </span>
                        </div>
                        <div className="min-w-0 flex-1 pt-1.5 flex justify-between space-x-4 space-x-reverse">
                          <div>
                            <p className="text-sm text-gray-500">
                              حكم صادر{' '}
                              <span className="font-medium text-gray-900">حكم رقم {2024000 + index}</span>
                            </p>
                          </div>
                          <div className="text-left text-sm whitespace-nowrap text-gray-500">
                            <time>منذ {index + 2} أيام</time>
                          </div>
                        </div>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Header Component
const Header = ({ user, onMenuToggle, onLogout }) => {
  const [showUserMenu, setShowUserMenu] = useState(false);

  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <button onClick={onMenuToggle} className="p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 lg:hidden">
              <Menu className="h-6 w-6" />
            </button>
            <div className="flex-shrink-0 flex items-center ml-4 lg:ml-0">
              <Scale className="h-8 w-8 text-blue-600 ml-2" />
              <h1 className="text-xl font-bold text-gray-900 mr-3">نظام الأحكام القضائية</h1>
            </div>
          </div>

          <div className="flex items-center space-x-4 space-x-reverse">
            <div className="hidden md:block">
              <div className="relative">
                <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                  <Search className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  type="text"
                  placeholder="البحث..."
                  className="block w-full pr-10 pl-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
            </div>

            <div className="relative">
              <button
                onClick={() => setShowUserMenu(!showUserMenu)}
                className="flex items-center text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                <img
                  className="h-8 w-8 rounded-full bg-gray-300"
                  src={`https://ui-avatars.com/api/?name=${encodeURIComponent(user?.name || 'المستخدم')}&background=3b82f6&color=fff`}
                  alt={user?.name}
                />
                <span className="hidden md:block mr-2 text-gray-700">{user?.name}</span>
                <ChevronDown className="h-4 w-4 text-gray-500 mr-1" />
              </button>

              {showUserMenu && (
                <div className="origin-top-right absolute left-0 mt-2 w-48 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5">
                  <button
                    onClick={onLogout}
                    className="flex items-center w-full text-right px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                  >
                    <LogOut className="h-4 w-4 ml-2" />
                    تسجيل الخروج
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

// Sidebar Component
const Sidebar = ({ isOpen, currentPage, onPageChange }) => {
  const menuItems = [
    { id: 'dashboard', title: 'لوحة التحكم', icon: BarChart3, path: 'dashboard' },
    { id: 'cases', title: 'القضايا', icon: FileText, path: 'cases' },
    { id: 'judgments', title: 'الأحكام', icon: Gavel, path: 'judgments' },
    { id: 'documents', title: 'الوثائق', icon: BookOpen, path: 'documents' },
    { id: 'courts', title: 'المحاكم', icon: Building, path: 'courts' },
    { id: 'users', title: 'المستخدمون', icon: Users, path: 'users' },
    { id: 'search', title: 'البحث المتقدم', icon: Search, path: 'search' }
  ];

  return (
    <div className={`fixed inset-y-0 right-0 z-50 w-64 bg-white shadow-lg transform ${isOpen ? 'translate-x-0' : 'translate-x-full'} transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0`}>
      <div className="flex flex-col h-full">
        <div className="flex items-center justify-center h-16 px-4 bg-gray-50 border-b border-gray-200">
          <Scale className="h-8 w-8 text-blue-600 ml-2" />
          <span className="text-lg font-semibold text-gray-900">نظام الأحكام</span>
        </div>
        
        <nav className="flex-1 px-2 py-4 bg-white overflow-y-auto">
          <div className="space-y-1">
            {menuItems.map((item) => {
              const isActive = currentPage === item.path;
              return (
                <button
                  key={item.id}
                  onClick={() => onPageChange(item.path)}
                  className={`group flex items-center w-full px-2 py-2 text-sm font-medium rounded-md transition-colors ${
                    isActive 
                      ? 'bg-blue-100 text-blue-900 border-l-4 border-blue-500' 
                      : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                  }`}
                >
                  <item.icon className={`ml-3 flex-shrink-0 h-6 w-6 ${isActive ? 'text-blue-500' : 'text-gray-400 group-hover:text-gray-500'}`} />
                  {item.title}
                </button>
              );
            })}
          </div>
        </nav>
      </div>
    </div>
  );
};

// Main App Component
const App = () => {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { user, loading, logout } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (!user) {
    return <LoginPage />;
  }

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard />;
      case 'cases':
        return <CasesList />;
      default:
        return <div className="p-8 text-center text-gray-500">صفحة {currentPage} قيد التطوير</div>;
    }
  };

  return (
    <div className="h-screen flex overflow-hidden bg-gray-100" dir="rtl">
      <Sidebar 
        isOpen={sidebarOpen} 
        currentPage={currentPage} 
        onPageChange={setCurrentPage} 
      />
      
      {sidebarOpen && (
        <div 
          className="fixed inset-0 z-40 lg:hidden" 
          onClick={() => setSidebarOpen(false)}
        >
          <div className="absolute inset-0 bg-gray-600 opacity-75"></div>
        </div>
      )}

      <div className="flex flex-col w-0 flex-1 overflow-hidden">
        <Header 
          user={user} 
          onMenuToggle={() => setSidebarOpen(!sidebarOpen)}
          onLogout={logout}
        />
        
        <main className="flex-1 relative overflow-y-auto focus:outline-none">
          <div className="py-6">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
              {renderPage()}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default function ArabicLegalJudgmentSystem() {
  return (
    <AuthProvider>
      <App />
    </AuthProvider>
  );
}