#pragma once

#include <vector>

#include <BaseClientRpc.h>
#include <Base.pb.h>

namespace kinova_kinematics_cpp
{

class KinovaKinematics
{
public:

    explicit KinovaKinematics(
        Kinova::Api::Base::BaseClient& base);

    std::vector<double> computeIK(
        double x,
        double y,
        double z,
        double theta_x,
        double theta_y,
        double theta_z);

private:

    Kinova::Api::Base::BaseClient& base_;
};

}
