import API from './api';

class CaseService {
  // Get all cases with pagination and filters
  getCases = async (params = {}) => {
    try {
      const response = await API.get('/cases', { params });
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'حدث خطأ في جلب القضايا',
      };
    }
  };

  // Get case by ID
  getCaseById = async (id) => {
    try {
      const response = await API.get(`/cases/${id}`);
      return {
        success: true,
        data: response.data.case,
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'حدث خطأ في جلب تفاصيل القضية',
      };
    }
  };

  // Create new case
  createCase = async (caseData) => {
    try {
      const response = await API.post('/cases', caseData);
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'حدث خطأ في إنشاء القضية',
      };
    }
  };

  // Update case
  updateCase = async (id, caseData) => {
    try {
      const response = await API.put(`/cases/${id}`, caseData);
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'حدث خطأ في تحديث القضية',
      };
    }
  };

  // Delete case
  deleteCase = async (id) => {
    try {
      const response = await API.delete(`/cases/${id}`);
      return {
        success: true,
        message: response.data.message,
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'حدث خطأ في حذف القضية',
      };
    }
  };

  // Search cases
  searchCases = async (query, filters = {}) => {
    try {
      const params = { q: query, ...filters };
      const response = await API.get('/cases/search', { params });
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'حدث خطأ في البحث',
      };
    }
  };

  // Get case statistics
  getCaseStatistics = async (filters = {}) => {
    try {
      const response = await API.get('/cases/statistics', { params: filters });
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'حدث خطأ في جلب الإحصائيات',
      };
    }
  };

  // Get categories
  getCategories = async () => {
    try {
      const response = await API.get('/categories');
      return {
        success: true,
        data: response.data.categories,
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'حدث خطأ في جلب الفئات',
      };
    }
  };

  // Get courts
  getCourts = async () => {
    try {
      const response = await API.get('/courts');
      return {
        success: true,
        data: response.data.courts,
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'حدث خطأ في جلب المحاكم',
      };
    }
  };
}

export const caseService = new CaseService();
