import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Paper,
  List,
  ListItem,
  ListItemText,
  Divider,
  Chip,
  Avatar,
  IconButton,
  Button,
} from '@mui/material';
import {
  TrendingUp,
  AccountBalance as AccountBalanceIcon,
  Gavel as GavelIcon,
  Description as DescriptionIcon,
  People as PeopleIcon,
  MoreVert as MoreVertIcon,
  Add as AddIcon,
  Visibility as VisibilityIcon,
} from '@mui/icons-material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
} from 'recharts';
import { useNavigate } from 'react-router-dom';
import { useQuery } from 'react-query';

import { caseService } from '../../services/caseService';
import { useAuth } from '../../contexts/AuthContext';

// Colors for charts
const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

const Dashboard = () => {
  const navigate = useNavigate();
  const { user } = useAuth();

  // Fetch dashboard statistics
  const { data: stats, isLoading: statsLoading } = useQuery(
    'dashboardStats',
    () => caseService.getCaseStatistics(),
    {
      refetchInterval: 5 * 60 * 1000, // Refetch every 5 minutes
    }
  );

  // Fetch recent cases
  const { data: recentCases, isLoading: casesLoading } = useQuery(
    'recentCases',
    () => caseService.getCases({ per_page: 5, sort: 'created_at', order: 'desc' }),
  );

  // Mock data for charts (replace with real data from API)
  const monthlyData = [
    { name: 'يناير', cases: 65, judgments: 45 },
    { name: 'فبراير', cases: 59, judgments: 52 },
    { name: 'مارس', cases: 80, judgments: 68 },
    { name: 'أبريل', cases: 81, judgments: 72 },
    { name: 'مايو', cases: 56, judgments: 48 },
    { name: 'يونيو', cases: 55, judgments: 61 },
  ];

  const statusData = [
    { name: 'جديدة', value: 45, color: '#2196f3' },
    { name: 'قيد النظر', value: 30, color: '#ff9800' },
    { name: 'محكومة', value: 20, color: '#4caf50' },
    { name: 'مؤجلة', value: 5, color: '#f44336' },
  ];

  const StatCard = ({ title, value, icon, color, subtitle, onClick }) => (
    <Card sx={{ height: '100%', cursor: onClick ? 'pointer' : 'default' }} onClick={onClick}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Box>
            <Typography color="textSecondary" gutterBottom variant="h6">
              {title}
            </Typography>
            <Typography variant="h4" component="h2" sx={{ fontWeight: 600, color }}>
              {value}
            </Typography>
            {subtitle && (
              <Typography color="textSecondary" variant="body2">
                {subtitle}
              </Typography>
            )}
          </Box>
          <Avatar sx={{ bgcolor: color, width: 60, height: 60 }}>
            {icon}
          </Avatar>
        </Box>
      </CardContent>
    </Card>
  );

  return (
    <Box>
      {/* Welcome Header */}
      <Paper sx={{ p: 3, mb: 3, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
        <Typography variant="h4" sx={{ fontWeight: 600, mb: 1 }}>
          مرحباً، {user?.full_name || 'المستخدم'}
        </Typography>
        <Typography variant="body1" sx={{ opacity: 0.9 }}>
          نظرة عامة على النشاط الحالي في النظام
        </Typography>
      </Paper>

      {/* Statistics Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="إجمالي القضايا"
            value={stats?.data?.statistics?.total_cases || 0}
            icon={<AccountBalanceIcon />}
            color="#2196f3"
            subtitle="في النظام"
            onClick={() => navigate('/cases')}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="الأحكام الصادرة"
            value="156"
            icon={<GavelIcon />}
            color="#4caf50"
            subtitle="هذا الشهر"
            onClick={() => navigate('/judgments')}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="المستندات"
            value="1,234"
            icon={<DescriptionIcon />}
            color="#ff9800"
            subtitle="مرفوعة"
            onClick={() => navigate('/documents')}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="المستخدمون"
            value="48"
            icon={<PeopleIcon />}
            color="#9c27b0"
            subtitle="نشطون"
          />
        </Grid>
      </Grid>

      {/* Charts Row */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        {/* Monthly Trends */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                الاتجاه الشهري للقضايا والأحكام
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={monthlyData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="cases" fill="#2196f3" name="القضايا" />
                  <Bar dataKey="judgments" fill="#4caf50" name="الأحكام" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Status Distribution */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                توزيع حالة القضايا
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={statusData}
                    cx="50%"
                    cy="50%"
                    outerRadius={80}
                    dataKey="value"
                    label={({ name, value }) => `${name}: ${value}`}
                  >
                    {statusData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Recent Activities */}
      <Grid container spacing={3}>
        {/* Recent Cases */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  القضايا الحديثة
                </Typography>
                <Button
                  size="small"
                  endIcon={<AddIcon />}
                  onClick={() => navigate('/cases/create')}
                >
                  إضافة قضية
                </Button>
              </Box>
              
              {casesLoading ? (
                <Typography>جاري التحميل...</Typography>
              ) : (
                <List>
                  {recentCases?.data?.cases?.slice(0, 5).map((case_, index) => (
                    <React.Fragment key={case_.id}>
                      <ListItem
                        sx={{ px: 0 }}
                        secondaryAction={
                          <IconButton onClick={() => navigate(`/cases/${case_.id}`)}>
                            <VisibilityIcon />
                          </IconButton>
                        }
                      >
                        <ListItemText
                          primary={case_.title}
                          secondary={
                            <Box>
                              <Typography variant="body2" color="textSecondary">
                                رقم القضية: {case_.case_number}
                              </Typography>
                              <Chip
                                label={case_.status}
                                size="small"
                                color={
                                  case_.status === 'جديدة' ? 'primary' :
                                  case_.status === 'قيد النظر' ? 'warning' :
                                  case_.status === 'محكومة' ? 'success' : 'default'
                                }
                                sx={{ mt: 1 }}
                              />
                            </Box>
                          }
                        />
                      </ListItem>
                      {index < 4 && <Divider />}
                    </React.Fragment>
                  )) || (
                    <Typography color="textSecondary">
                      لا توجد قضايا حديثة
                    </Typography>
                  )}
                </List>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Quick Actions */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                الإجراءات السريعة
              </Typography>
              
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={<AccountBalanceIcon />}
                    onClick={() => navigate('/cases/create')}
                    sx={{ py: 1.5 }}
                  >
                    قضية جديدة
                  </Button>
                </Grid>
                <Grid item xs={6}>
                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={<GavelIcon />}
                    onClick={() => navigate('/judgments/create')}
                    sx={{ py: 1.5 }}
                  >
                    حكم جديد
                  </Button>
                </Grid>
                <Grid item xs={6}>
                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={<DescriptionIcon />}
                    onClick={() => navigate('/documents')}
                    sx={{ py: 1.5 }}
                  >
                    رفع مستند
                  </Button>
                </Grid>
                <Grid item xs={6}>
                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={<TrendingUp />}
                    onClick={() => navigate('/reports')}
                    sx={{ py: 1.5 }}
                  >
                    عرض التقارير
                  </Button>
                </Grid>
              </Grid>

              <Divider sx={{ my: 3 }} />

              {/* Recent Activity Log */}
              <Typography variant="subtitle1" sx={{ mb: 2, fontWeight: 600 }}>
                النشاط الأخير
              </Typography>
              
              <List dense>
                <ListItem sx={{ px: 0 }}>
                  <ListItemText
                    primary="تم إنشاء قضية جديدة"
                    secondary="منذ 30 دقيقة"
                  />
                </ListItem>
                <ListItem sx={{ px: 0 }}>
                  <ListItemText
                    primary="تم رفع مستند جديد"
                    secondary="منذ ساعة واحدة"
                  />
                </ListItem>
                <ListItem sx={{ px: 0 }}>
                  <ListItemText
                    primary="تم إصدار حكم جديد"
                    secondary="منذ 3 ساعات"
                  />
                </ListItem>
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
