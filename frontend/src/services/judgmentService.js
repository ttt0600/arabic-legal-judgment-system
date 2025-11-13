import API from './api';

class JudgmentService {
  // Get all judgments with pagination and filters
  getJudgments = async (params = {}) => {
    try {
      const response = await API.get('/judgments', { params });
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'حدث خطأ في جلب الأحكام',
      };
    }
  };

  // Get judgment by ID
  getJudgmentById = async (id) => {
    try {
      const response = await API.get(`/judgments/${id}`);
      return {
        success: true,
        data: response.data.judgment,
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'حدث خطأ في جلب تفاصيل الحكم',
      };
    }
  };

  // Create new judgment
  createJudgment = async (judgmentData) => {
    try {
      const response = await API.post('/judgments', judgmentData);
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'حدث خطأ في إنشاء الحكم',
      };
    }
  };

  // Update judgment
  updateJudgment = async (id, judgmentData) => {
    try {
      const response = await API.put(`/judgments/${id}`, judgmentData);
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'حدث خطأ في تحديث الحكم',
      };
    }
  };

  // Delete judgment
  deleteJudgment = async (id) => {
    try {
      const response = await API.delete(`/judgments/${id}`);
      return {
        success: true,
        message: response.data.message,
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'حدث خطأ في حذف الحكم',
      };
    }
  };

  // Search judgments
  searchJudgments = async (query, filters = {}) => {
    try {
      const params = { q: query, ...filters };
      const response = await API.get('/judgments/search', { params });
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

  // Get judgment statistics
  getJudgmentStatistics = async (filters = {}) => {
    try {
      const response = await API.get('/judgments/statistics', { params: filters });
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
}

export const judgmentService = new JudgmentService();
