#include <memory>
#include <iostream>

#include <rclcpp/rclcpp.hpp>

#include "kinova_sdk_bridge/srv/compute_ik.hpp"

#include <TransportClientTcp.h>
#include <RouterClient.h>
#include <SessionManager.h>
#include <BaseClientRpc.h>
#include <Session.pb.h>

namespace k_api = Kinova::Api;

class IKService : public rclcpp::Node
{
public:

    IKService()
    : Node("kinova_sdk_bridge")
    {
        robot_ip_ = declare_parameter("robot_ip","192.168.1.10");
        username_ = declare_parameter("username","estudiantes");
        password_ = declare_parameter("password","KINOVA-UMNG");

        connect();

        service_ =
            create_service<kinova_sdk_bridge::srv::ComputeIK>(
                "compute_inverse_kinematics",
                std::bind(
                    &IKService::callback,
                    this,
                    std::placeholders::_1,
                    std::placeholders::_2));

        RCLCPP_INFO(get_logger(),"IK service ready");
    }

private:

    void connect()
    {
        transport_ =
            std::make_unique<k_api::TransportClientTcp>();

        router_ =
            std::make_unique<k_api::RouterClient>(
                transport_.get(),
                [](k_api::KError err)
                {
                    std::cout << err.toString() << std::endl;
                });

        session_ =
            std::make_unique<k_api::SessionManager>(
                router_.get());

        base_ =
            std::make_unique<k_api::Base::BaseClient>(
                router_.get());

        transport_->connect(robot_ip_,10000);

        k_api::Session::CreateSessionInfo info;

        info.set_username(username_);
        info.set_password(password_);
        info.set_session_inactivity_timeout(10000);
        info.set_connection_inactivity_timeout(2000);

        session_->CreateSession(info);
    }

    void callback(
        const std::shared_ptr<
            kinova_sdk_bridge::srv::ComputeIK::Request> req,

        std::shared_ptr<
            kinova_sdk_bridge::srv::ComputeIK::Response> res)
    {
        try
        {
            k_api::Base::IKData data;

            auto pose =
                data.mutable_cartesian_pose();

            pose->set_x(req->pose.position.x);
            pose->set_y(req->pose.position.y);
            pose->set_z(req->pose.position.z);

            //
            // POR AHORA
            //
            // usamos orientación fija
            //

            pose->set_theta_x(180);
            pose->set_theta_y(0);
            pose->set_theta_z(90);
/*
            auto guess = data.mutable_guess();

            for(int i=0;i<6;i++)
            {
                auto joint =
                    guess->add_joint_angles();

                joint->set_joint_identifier(i+1);
                joint->set_value(0.0);
            }
*/
            //mejora para no comenzar desde 0.0
            auto guess = data.mutable_guess();

            for (size_t i = 0; i < req->guess.size(); i++)
            {
                auto joint = guess->add_joint_angles();

                joint->set_joint_identifier(i + 1);
                joint->set_value(req->guess[i]);
            }


            auto solution =
                base_->ComputeInverseKinematics(data);

            res->joint1 =
                solution.joint_angles(0).value();

            res->joint2 =
                solution.joint_angles(1).value();

            res->joint3 =
                solution.joint_angles(2).value();

            res->joint4 =
                solution.joint_angles(3).value();

            res->joint5 =
                solution.joint_angles(4).value();

            res->joint6 =
                solution.joint_angles(5).value();

            res->success = true;
            res->message = "OK";
        }
        catch(const k_api::KDetailedException& ex)
        {
            res->success = false;
            res->message = ex.what();
        }
    }

    std::string robot_ip_;
    std::string username_;
    std::string password_;

    std::unique_ptr<k_api::TransportClientTcp> transport_;
    std::unique_ptr<k_api::RouterClient> router_;
    std::unique_ptr<k_api::SessionManager> session_;
    std::unique_ptr<k_api::Base::BaseClient> base_;

    rclcpp::Service<
        kinova_sdk_bridge::srv::ComputeIK>::SharedPtr service_;
};

int main(int argc,char **argv)
{
    rclcpp::init(argc,argv);

    rclcpp::spin(
        std::make_shared<IKService>());

    rclcpp::shutdown();

    return 0;
}
