#include <iostream>
#include <string>

#include <TransportClientTcp.h>
#include <RouterClient.h>
#include <SessionManager.h>
#include <BaseClientRpc.h>

#include <Session.pb.h>


namespace k_api = Kinova::Api;


int main(int argc, char **argv)
{
    std::string robot_ip = "192.168.1.10";
    std::string username = "estudiantes";
    std::string password = "KINOVA-UMNG";


    std::cout << "Starting Kinova SDK connection test" 
              << std::endl;


    try
    {
        /*
         * TCP transport
         */
        k_api::TransportClientTcp transport;


        /*
         * Router
         */
        k_api::RouterClient router(
            &transport,
            [](k_api::KError error)
            {
                std::cout 
                    << "Router error: "
                    << error.toString()
                    << std::endl;
            });


        /*
         * Session manager
         */
        k_api::SessionManager session_manager(&router);


        /*
         * Base client
         */
        k_api::Base::BaseClient base(&router);



        std::cout 
            << "Connecting to robot..."
            << std::endl;


        transport.connect(
            robot_ip,
            10000);



        /*
         * Create session
         */
        k_api::Session::CreateSessionInfo session_info;


        session_info.set_username(username);
        session_info.set_password(password);

        session_info.set_session_inactivity_timeout(
            10000);

        session_info.set_connection_inactivity_timeout(
            2000);



        std::cout 
            << "Creating session..."
            << std::endl;


        session_manager.CreateSession(session_info);


        std::cout 
            << "Session created"
            << std::endl;



        /*
         * First SDK command
         */
        auto count = base.GetActuatorCount();


        std::cout
            << "Actuators detected: "
            << count.count()
            << std::endl;

        
        std::cout 
            << "Testing inverse kinematics..."
            << std::endl;


        //k_api::Base::IKData ik_data;
       
        Kinova::Api::Base::IKData ik_data;

        auto pose = ik_data.mutable_cartesian_pose();


        // posición en metros
        pose->set_x(0.40);
        pose->set_y(0.10);
        pose->set_z(0.20);


        // orientación en grados
        pose->set_theta_x(180);
        pose->set_theta_y(0);
        pose->set_theta_z(90);

        auto guess = ik_data.mutable_guess();

        for(int i=0;i<6;i++)
        {
            auto joint = guess->add_joint_angles();

            joint->set_joint_identifier(i+1);
            joint->set_value(0.0);
        }



        try
        {

            std::cout
    << "IK request with guess:"
    << std::endl
    << ik_data.DebugString()
    << std::endl;

            std::cout << "\nReceived guess\n";

            for (int i = 0; i < guess->joint_angles_size(); i++)
            {
                std::cout
                    << "Joint "
                    << i + 1
                    << ": "
                    << guess->joint_angles(i).value()
                    << std::endl;   

    
            auto solution = base.ComputeInverseKinematics(
                ik_data
            );


            std::cout
                << "IK solution found"
                << std::endl;


            for(
                int i = 0;
                i < solution.joint_angles_size();
                i++)
            {

                std::cout
                    << "Joint "
                    << i+1
                    << ": "
                    << solution.joint_angles(i).value()
                    << " deg"
                    << std::endl;

            }

        }
        catch(
            const k_api::KDetailedException& ex)
        {

            std::cerr
                << "IK failed"
                << std::endl;


            std::cerr
                << ex.what()
                << std::endl;

        }


        /*
         * Close session
         */
        session_manager.CloseSession();


        transport.disconnect();


        std::cout
            << "Test finished successfully"
            << std::endl;


    }
    catch(const std::exception& e)
    {
        std::cerr
            << "Exception: "
            << e.what()
            << std::endl;

        return -1;
    }


    return 0;
}
