import React, { useState, useEffect } from 'react';
import './DataViewer.css';

const DataViewer = ({ onBack }) => {
  const [judgments, setJudgments] = useState([]);
  const [filteredJudgments, setFilteredJudgments] = useState([]);
  const [headers, setHeaders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(10);
  const [selectedJudgment, setSelectedJudgment] = useState(null);
  const [sortField, setSortField] = useState('');
  const [sortDirection, setSortDirection] = useState('asc');

  useEffect(() => {
    fetchJudgments();
  }, []);

  useEffect(() => {
    // تطبيق البحث والفلترة
    let filtered = judgments;
    
    if (searchTerm) {
      filtered = judgments.filter(judgment => {
        return Object.values(judgment).some(value => 
          String(value).toLowerCase().includes(searchTerm.toLowerCase())
        );
      });
    }

    // تطبيق الترتيب
    if (sortField) {
      filtered.sort((a, b) => {
        const aValue = String(a[sortField] || '');
        const bValue = String(b[sortField] || '');
        
        if (sortDirection === 'asc') {
          return aValue.localeCompare(bValue);
        } else {
          return bValue.localeCompare(aValue);
        }
      });
    }

    setFilteredJudgments(filtered);
    setCurrentPage(1); // إعادة تعيين الصفحة عند البحث
  }, [judgments, searchTerm, sortField, sortDirection]);

  const fetchJudgments = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:5000/api/judgments');
      const data = await response.json();
      
      if (data.success) {
        setJudgments(data.judgments);
        setHeaders(data.headers || []);
      }
    } catch (error) {
      console.error('خطأ في جلب البيانات:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSort = (field) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('asc');
    }
  };

  const exportToJSON = () => {
    const dataStr = JSON.stringify(filteredJudgments, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = `arabic_legal_judgments_${new Date().toISOString().split('T')[0]}.json`;
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  const exportToCSV = () => {
    if (filteredJudgments.length === 0) return;
    
    const csvHeaders = headers.join(',');
    const csvRows = filteredJudgments.map(judgment => 
      headers.map(header => `"${String(judgment[header] || '').replace(/"/g, '""')}"`).join(',')
    );
    
    const csvContent = [csvHeaders, ...csvRows].join('\n');
    const dataUri = 'data:text/csv;charset=utf-8-bom,\ufeff' + csvContent;
    
    const exportFileDefaultName = `arabic_legal_judgments_${new Date().toISOString().split('T')[0]}.csv`;
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  // حساب البيانات للصفحة الحالية
  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = filteredJudgments.slice(indexOfFirstItem, indexOfLastItem);
  const totalPages = Math.ceil(filteredJudgments.length / itemsPerPage);

  if (loading) {
    return (
      <div className="data-viewer">
        <div className="loading">
          <div className="spinner"></div>
          <p>جاري تحميل البيانات...</p>
        </div>
      </div>
    );
  }

  if (selectedJudgment) {
    return (
      <div className="data-viewer">
        <div className="judgment-detail">
          <div className="detail-header">
            <button className="btn-back" onClick={() => setSelectedJudgment(null)}>
              ← العودة للقائمة
            </button>
            <h2>تفاصيل الحكم</h2>
          </div>
          
          <div className="detail-content">
            {headers.map(header => (
              <div key={header} className="detail-field">
                <strong>{header}:</strong>
                <div className="field-value">
                  {selectedJudgment[header] || 'غير محدد'}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="data-viewer">
      {/* Header */}
      <div className="viewer-header">
        <div className="header-top">
          <button className="btn-back" onClick={onBack}>← العودة</button>
          <h1>🗄️ عارض البيانات القانونية</h1>
          <div className="data-stats">
            <span>{filteredJudgments.length} من {judgments.length} حكم</span>
          </div>
        </div>
        
        {/* أدوات البحث والتصفية */}
        <div className="tools-bar">
          <div className="search-box">
            <input
              type="text"
              placeholder="🔍 البحث في جميع الحقول..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          
          <div className="action-buttons">
            <button className="btn-export" onClick={exportToJSON}>
              📄 تصدير JSON
            </button>
            <button className="btn-export" onClick={exportToCSV}>
              📊 تصدير CSV
            </button>
            <button className="btn-refresh" onClick={fetchJudgments}>
              🔄 تحديث
            </button>
          </div>
        </div>
      </div>

      {/* جدول البيانات */}
      <div className="data-table-container">
        {currentItems.length > 0 ? (
          <table className="data-table">
            <thead>
              <tr>
                <th width="50">#</th>
                {headers.slice(0, 5).map(header => (
                  <th 
                    key={header} 
                    onClick={() => handleSort(header)}
                    className={`sortable ${sortField === header ? `sorted-${sortDirection}` : ''}`}
                  >
                    {header}
                    {sortField === header && (
                      <span className="sort-indicator">
                        {sortDirection === 'asc' ? ' ↑' : ' ↓'}
                      </span>
                    )}
                  </th>
                ))}
                <th width="120">الإجراءات</th>
              </tr>
            </thead>
            <tbody>
              {currentItems.map((judgment, index) => (
                <tr key={index} className="data-row">
                  <td>{indexOfFirstItem + index + 1}</td>
                  {headers.slice(0, 5).map(header => (
                    <td key={header}>
                      <div className="cell-content">
                        {String(judgment[header] || '').length > 100 
                          ? String(judgment[header]).substring(0, 100) + '...'
                          : judgment[header] || 'غير محدد'
                        }
                      </div>
                    </td>
                  ))}
                  <td>
                    <button 
                      className="btn-view"
                      onClick={() => setSelectedJudgment(judgment)}
                    >
                      👁️ عرض
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className="no-results">
            <h3>لا توجد نتائج</h3>
            <p>لم يتم العثور على أحكام تطابق معايير البحث</p>
          </div>
        )}
      </div>

      {/* أدوات التنقل بين الصفحات */}
      {totalPages > 1 && (
        <div className="pagination">
          <button 
            onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
            disabled={currentPage === 1}
            className="pagination-btn"
          >
            ← السابق
          </button>
          
          <div className="page-info">
            <span>صفحة {currentPage} من {totalPages}</span>
            <select 
              value={currentPage} 
              onChange={(e) => setCurrentPage(Number(e.target.value))}
            >
              {Array.from({ length: totalPages }, (_, i) => (
                <option key={i + 1} value={i + 1}>
                  {i + 1}
                </option>
              ))}
            </select>
          </div>
          
          <button 
            onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
            disabled={currentPage === totalPages}
            className="pagination-btn"
          >
            التالي →
          </button>
        </div>
      )}
    </div>
  );
};

export default DataViewer;
