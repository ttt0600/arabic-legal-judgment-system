import React, { useState } from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import {
  Box,
  Drawer,
  AppBar,
  Toolbar,
  List,
  Typography,
  Divider,
  IconButton,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Avatar,
  Menu,
  MenuItem,
  Badge,
  Tooltip,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Dashboard as DashboardIcon,
  Gavel as GavelIcon,
  Description as DescriptionIcon,
  Search as SearchIcon,
  Assessment as AssessmentIcon,
  Settings as SettingsIcon,
  Person as PersonIcon,
  Logout as LogoutIcon,
  Notifications as NotificationsIcon,
  ChevronLeft as ChevronLeftIcon,
  ChevronRight as ChevronRightIcon,
  AccountBalance as AccountBalanceIcon,
  Folder as FolderIcon,
} from '@mui/icons-material';

import { useAuth } from '../../contexts/AuthContext';

const drawerWidth = 280;

// Navigation items
const navigationItems = [
  {
    text: 'لوحة التحكم',
    icon: <DashboardIcon />,
    path: '/dashboard',
    permission: null,
  },
  {
    text: 'القضايا',
    icon: <AccountBalanceIcon />,
    path: '/cases',
    permission: 'view_cases',
  },
  {
    text: 'الأحكام',
    icon: <GavelIcon />,
    path: '/judgments',
    permission: 'view_judgments',
  },
  {
    text: 'المستندات',
    icon: <FolderIcon />,
    path: '/documents',
    permission: 'view_documents',
  },
  {
    text: 'البحث',
    icon: <SearchIcon />,
    path: '/search',
    permission: null,
  },
  {
    text: 'التقارير',
    icon: <AssessmentIcon />,
    path: '/reports',
    permission: 'view_reports',
  },
  {
    text: 'الإعدادات',
    icon: <SettingsIcon />,
    path: '/settings',
    permission: 'manage_settings',
  },
];

const Layout = () => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [collapsed, setCollapsed] = useState(false);
  const [anchorEl, setAnchorEl] = useState(null);
  
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout, hasPermission } = useAuth();

  // Handle drawer toggle for mobile
  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  // Handle drawer collapse for desktop
  const handleDrawerCollapse = () => {
    setCollapsed(!collapsed);
  };

  // Handle user menu
  const handleUserMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleUserMenuClose = () => {
    setAnchorEl(null);
  };

  // Handle logout
  const handleLogout = async () => {
    await logout();
    navigate('/login');
    handleUserMenuClose();
  };

  // Handle navigation
  const handleNavigation = (path) => {
    navigate(path);
    if (mobileOpen) {
      setMobileOpen(false);
    }
  };

  // Check if path is active
  const isActive = (path) => {
    return location.pathname === path || location.pathname.startsWith(`${path}/`);
  };

  // Filter navigation items based on permissions
  const filteredNavigationItems = navigationItems.filter(item => {
    if (!item.permission) return true;
    return hasPermission(item.permission);
  });

  // Drawer content
  const drawer = (
    <div>
      {/* Logo and Title */}
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          padding: 2,
          minHeight: 64,
        }}
      >
        <AccountBalanceIcon sx={{ mr: 2, color: 'primary.main' }} />
        {!collapsed && (
          <Typography variant="h6" sx={{ fontWeight: 600 }}>
            نظام الأحكام القانونية
          </Typography>
        )}
      </Box>
      
      <Divider />

      {/* Navigation Items */}
      <List>
        {filteredNavigationItems.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton
              onClick={() => handleNavigation(item.path)}
              selected={isActive(item.path)}
              sx={{
                minHeight: 48,
                justifyContent: collapsed ? 'center' : 'initial',
                px: 2.5,
              }}
            >
              <ListItemIcon
                sx={{
                  minWidth: 0,
                  mr: collapsed ? 'auto' : 3,
                  justifyContent: 'center',
                }}
              >
                {item.icon}
              </ListItemIcon>
              {!collapsed && (
                <ListItemText
                  primary={item.text}
                  primaryTypographyProps={{
                    fontSize: '0.9rem',
                    fontWeight: isActive(item.path) ? 600 : 400,
                  }}
                />
              )}
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </div>
  );

  return (
    <Box sx={{ display: 'flex', height: '100vh' }}>
      {/* App Bar */}
      <AppBar
        position="fixed"
        sx={{
          width: { sm: `calc(100% - ${collapsed ? 73 : drawerWidth}px)` },
          ml: { sm: `${collapsed ? 73 : drawerWidth}px` },
          transition: 'width 0.3s, margin 0.3s',
        }}
      >
        <Toolbar>
          {/* Mobile menu button */}
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>

          {/* Desktop collapse button */}
          <IconButton
            color="inherit"
            onClick={handleDrawerCollapse}
            sx={{ mr: 2, display: { xs: 'none', sm: 'block' } }}
          >
            {collapsed ? <ChevronRightIcon /> : <ChevronLeftIcon />}
          </IconButton>

          {/* Page Title */}
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            {navigationItems.find(item => isActive(item.path))?.text || 'نظام الأحكام القانونية'}
          </Typography>

          {/* Notifications */}
          <Tooltip title="الإشعارات">
            <IconButton color="inherit" sx={{ mr: 1 }}>
              <Badge badgeContent={4} color="error">
                <NotificationsIcon />
              </Badge>
            </IconButton>
          </Tooltip>

          {/* User Menu */}
          <Tooltip title="الملف الشخصي">
            <IconButton onClick={handleUserMenuOpen} sx={{ p: 0 }}>
              <Avatar sx={{ width: 32, height: 32, bgcolor: 'secondary.main' }}>
                {user?.full_name?.charAt(0) || 'م'}
              </Avatar>
            </IconButton>
          </Tooltip>

          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleUserMenuClose}
            anchorOrigin={{
              vertical: 'bottom',
              horizontal: 'left',
            }}
            transformOrigin={{
              vertical: 'top',
              horizontal: 'left',
            }}
          >
            <MenuItem onClick={() => { navigate('/profile'); handleUserMenuClose(); }}>
              <ListItemIcon>
                <PersonIcon fontSize="small" />
              </ListItemIcon>
              الملف الشخصي
            </MenuItem>
            <Divider />
            <MenuItem onClick={handleLogout}>
              <ListItemIcon>
                <LogoutIcon fontSize="small" />
              </ListItemIcon>
              تسجيل الخروج
            </MenuItem>
          </Menu>
        </Toolbar>
      </AppBar>

      {/* Navigation Drawer */}
      <Box
        component="nav"
        sx={{ width: { sm: collapsed ? 73 : drawerWidth }, flexShrink: { sm: 0 } }}
      >
        {/* Mobile drawer */}
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true, // Better open performance on mobile
          }}
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': {
              boxSizing: 'border-box',
              width: drawerWidth,
            },
          }}
        >
          {drawer}
        </Drawer>

        {/* Desktop drawer */}
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': {
              boxSizing: 'border-box',
              width: collapsed ? 73 : drawerWidth,
              transition: 'width 0.3s',
              overflowX: 'hidden',
            },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>

      {/* Main Content */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${collapsed ? 73 : drawerWidth}px)` },
          transition: 'width 0.3s',
          backgroundColor: 'background.default',
          minHeight: '100vh',
          pt: 8, // Account for AppBar height
        }}
      >
        <Outlet />
      </Box>
    </Box>
  );
};

export default Layout;
