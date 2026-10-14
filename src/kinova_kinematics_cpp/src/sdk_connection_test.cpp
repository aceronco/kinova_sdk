

//este es para una prueba de concepto no muy fructifera
//el paquete kinova_sdk_test si fe fructifero

#include <iostream>

#include <TransportClientTcp.h>
#include <RouterClient.h>
#include <SessionManager.h>
#include <BaseClientRpc.h>

int main()
{
    KinovaConnection connection(
        "192.168.1.10",
        "estudiantes",
        "KINOVA-UMNG");

    std::cout << connection.base()
                     .GetActuatorCount()
                     .count()
              << std::endl;

    return 0;
}
