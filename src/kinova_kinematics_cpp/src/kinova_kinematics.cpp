#include "kinova_kinematics_cpp/kinova_kinematics.hpp"

#include <KDetailedException.h>

namespace kinova_kinematics_cpp
{

KinovaKinematics::KinovaKinematics(
    Kinova::Api::Base::BaseClient& base)
    : base_(base)
{
}

std::vector<double> KinovaKinematics::computeIK(
    double x,
    double y,
    double z,
    double theta_x,
    double theta_y,
    double theta_z)
{
    std::vector<double> joints;

    Kinova::Api::Base::IKData ik_data;

    auto pose = ik_data.mutable_cartesian_pose();

    pose->set_x(x);
    pose->set_y(y);
    pose->set_z(z);

    pose->set_theta_x(theta_x);
    pose->set_theta_y(theta_y);
    pose->set_theta_z(theta_z);

    try
    {
        auto solution = base_.ComputeInverseKinematics(ik_data);

        for (int i = 0; i < solution.joint_angles_size(); ++i)
        {
            joints.push_back(solution.joint_angles(i).value());
        }
    }
    catch (const Kinova::Api::KDetailedException& ex)
    {
        throw;
    }

    return joints;
}

}
