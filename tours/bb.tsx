import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Spin, Alert, Button, Tag, Divider, Image, Typography } from 'antd';
import { 
  UserOutlined, 
  TeamOutlined, 
  ReloadOutlined,
  CameraOutlined,
  InfoCircleOutlined 
} from '@ant-design/icons';
// Using fetch API instead of axios

const { Title, Text, Paragraph } = Typography;

type SafariPackage = {
  id: number;
  name: string;
  description: string;
  group_size_min: number;
  group_size_max: number;
  picture?: string;
  created_at?: string;
  updated_at?: string;
};

const SafariList: React.FC = () => {
  const [packages, setPackages] = useState<SafariPackage[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [refreshing, setRefreshing] = useState(false);

  // Function to fetch packages from Django backend
  const fetchPackages = async (showRefreshLoader = false) => {
    try {
      if (showRefreshLoader) {
        setRefreshing(true);
      } else {
        setLoading(true);
      }
      setError(null);

      const response = await fetch('http://127.0.0.1:8000/api/safari-packages', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setPackages(data);
    } catch (err: any) {
      console.error('Error fetching packages:', err);
      setError(
        err.message || 
        'Failed to fetch safari packages'
      );
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  // Initial load
  useEffect(() => {
    fetchPackages();
  }, []);

  // Auto-refresh every 30 seconds to catch new packages
  useEffect(() => {
    const interval = setInterval(() => {
      fetchPackages(true);
    }, 30000); // 30 seconds

    return () => clearInterval(interval);
  }, []);

  // Manual refresh handler
  const handleRefresh = () => {
    fetchPackages(true);
  };

  // Get image URL for display
  const getImageUrl = (picturePath: string | undefined) => {
    if (!picturePath) return null;
    
    // If it's already a full URL, return as is
    if (picturePath.startsWith('http')) {
      return picturePath;
    }
    
    // Otherwise, construct the full URL with your Django backend
    return `http://127.0.0.1:8000${picturePath}`;
  };

  if (loading && !refreshing) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <Spin size="large" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6">
        <Alert
          message="Error Loading Safari Packages"
          description={error}
          type="error"
          showIcon
          action={
            <Button size="small" type="primary" onClick={handleRefresh}>
              Retry
            </Button>
          }
        />
      </div>
    );
  }

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <Title level={1} className="mb-2">
              🦁 Safari Packages
            </Title>
            <Text type="secondary" className="text-lg">
              Discover amazing safari adventures ({packages.length} packages available)
            </Text>
          </div>
          <Button
            type="primary"
            icon={<ReloadOutlined spin={refreshing} />}
            onClick={handleRefresh}
            loading={refreshing}
            size="large"
          >
            Refresh
          </Button>
        </div>

        {/* Packages Grid */}
        {packages.length === 0 ? (
          <Card className="text-center py-12">
            <div className="text-gray-400 text-6xl mb-4">
              🏕️
            </div>
            <Title level={3} type="secondary">
              No Safari Packages Available
            </Title>
            <Text type="secondary">
              New packages will appear here automatically when they are added.
            </Text>
          </Card>
        ) : (
          <Row gutter={[24, 24]}>
            {packages.map((pkg) => (
              <Col xs={24} sm={12} lg={8} xl={6} key={pkg.id}>
                <Card
                  hoverable
                  className="h-full shadow-lg hover:shadow-xl transition-all duration-300"
                  cover={
                    pkg.picture ? (
                      <div className="h-48 overflow-hidden">
                        <Image
                          alt={pkg.name}
                          src={getImageUrl(pkg.picture)}
                          className="w-full h-full object-cover"
                          fallback="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMIAAADDCAYAAADQvc6UAAABRWlDQ1BJQ0MgUHJvZmlsZQAAKJFjYGASSSwoyGFhYGDIzSspCnJ3UoiIjFJgf8LAwSDCIMogwMCcmFxc4BgQ4ANUwgCjUcG3awyMIPqyLsis7PPOq3QdDFcvjV3jOD1boQVTPQrgSkktTgbSf4A4LbmgqISBgTEFyFYuLykAsTuAbJEioKOA7DkgdjqEvQHEToKwj4DVhAQ5A9k3gGyB5IxEoBmML4BsnSQk8XQkNtReEOBxcfXxUQg1Mjc0dyHgXNJBSWpFCYh2zi+oLMpMzyhRcASGUqqCZ16yno6CkYGRAQMDKMwhqj/fAIcloxgHQqxAjIHBEugw5sUIsSQpBobtQPdLciLEVJYzMPBHMDBsayhILEqEO4DxG0txmrERhM29nYGBddr//5/DGRjYNRkY/l7////39v///y4Dmn+LgeHANwDrkl1AuO+pmgAAADhlWElmTU0AKgAAAAgAAYdpAAQAAAABAAAAGgAAAAAAAqACAAQAAAABAAAAwqADAAQAAAABAAAAwwAAAAD9b/HnAAAHlklEQVR4Ae3dP3Ik1RnG4W+FgYxN4BMghRc+A5+BIXc2Nb4BQafgQC5sgQHCNs4+AXdmuIHlFQRcQrNOYVtb20jRu2k/YQ/aHRh0B/6/gJ3F5vFqZoM97A=="
                          preview={{
                            mask: <div className="text-white">
                              <CameraOutlined className="text-2xl" />
                            </div>
                          }}
                        />
                      </div>
                    ) : (
                      <div className="h-48 bg-gradient-to-br from-green-400 to-blue-500 flex items-center justify-center">
                        <div className="text-white text-6xl">🏞️</div>
                      </div>
                    )
                  }
                  actions={[
                    <div key="info" className="text-center">
                      <InfoCircleOutlined className="text-blue-500" />
                      <div className="text-xs mt-1">More Info</div>
                    </div>
                  ]}
                >
                  <div className="space-y-3">
                    {/* Package Name */}
                    <Title level={4} className="mb-2 line-clamp-2">
                      {pkg.name}
                    </Title>

                    {/* Description */}
                    <Paragraph 
                      ellipsis={{ rows: 3, expandable: true, symbol: 'more' }}
                      className="text-gray-600 text-sm"
                    >
                      {pkg.description}
                    </Paragraph>

                    <Divider className="my-3" />

                    {/* Group Size Info */}
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <UserOutlined className="text-gray-500" />
                        <Text strong className="text-sm">Group Size:</Text>
                      </div>
                      <Tag 
                        icon={<TeamOutlined />} 
                        color="blue"
                        className="flex items-center"
                      >
                        {pkg.group_size_min === pkg.group_size_max 
                          ? `${pkg.group_size_min} people`
                          : `${pkg.group_size_min}-${pkg.group_size_max} people`
                        }
                      </Tag>
                    </div>

                    {/* Package ID */}
                    <div className="flex items-center justify-between pt-2">
                      <Text type="secondary" className="text-xs">
                        Package #{pkg.id}
                      </Text>
                      {pkg.created_at && (
                        <Text type="secondary" className="text-xs">
                          Added: {new Date(pkg.created_at).toLocaleDateString()}
                        </Text>
                      )}
                    </div>
                  </div>
                </Card>
              </Col>
            ))}
          </Row>
        )}

        {/* Footer Info */}
        <div className="mt-12 text-center">
          <Text type="secondary">
            🔄 Packages automatically refresh every 30 seconds
          </Text>
        </div>
      </div>
    </div>
  );
};

export default SafariList;