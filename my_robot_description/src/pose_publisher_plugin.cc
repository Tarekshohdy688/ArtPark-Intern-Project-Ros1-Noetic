#include <ros/ros.h>
#include <gazebo/gazebo.hh>
#include <gazebo/physics/Model.hh>
#include <geometry_msgs/PoseStamped.h>
#include <ignition/math/Quaternion.hh>
#include <gazebo/physics/World.hh>


namespace gazebo
{
  class PosePublisherPlugin : public ModelPlugin
  {
  public:
    PosePublisherPlugin() : ModelPlugin()
    {
    }

    void Load(physics::ModelPtr model, sdf::ElementPtr sdf)
    {
      this->model = model;
      this->nodeHandle = new ros::NodeHandle("~");

      this->poseSub = this->nodeHandle->subscribe("/robot_pose", 10, &PosePublisherPlugin::PoseCallback, this);
    }

    void PoseCallback(const geometry_msgs::PoseStamped::ConstPtr& msg)
    {
      ignition::math::Pose3d pose(msg->pose.position.x, msg->pose.position.y, msg->pose.position.z,
                                  msg->pose.orientation.x, msg->pose.orientation.y, msg->pose.orientation.z, msg->pose.orientation.w);
      this->model->SetWorldPose(pose);
    }

  private:
    physics::ModelPtr model;
    ros::NodeHandle* nodeHandle;
    ros::Subscriber poseSub;
  };

  GZ_REGISTER_MODEL_PLUGIN(PosePublisherPlugin)
}
