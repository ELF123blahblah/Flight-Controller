#include "stm32f4xx_hal.h"

/* === Defines === */
#define RC_MIN 1000
#define RC_MAX 2000
#define MOTOR_MIN 1000
#define MOTOR_MAX 2000

/* === Handles === */
TIM_HandleTypeDef htim2;   // RC input
TIM_HandleTypeDef htim3;   // Motor PWM

/* === RC Channels === */
volatile uint16_t rc_throttle = 1000;
volatile uint16_t rc_roll     = 1500;
volatile uint16_t rc_pitch    = 1500;
volatile uint16_t rc_yaw      = 1500;

/* === Motor Outputs === */
uint16_t motor[4] = {1000, 1000, 1000, 1000};

/* === Function Prototypes === */
void SystemClock_Config(void);
void MX_TIM2_Init(void);
void MX_TIM3_Init(void);
void read_rc_inputs(void);
void flight_control_update(void);
void write_motor_outputs(void);

/* === Main === */
int main(void)
{
    HAL_Init();
    SystemClock_Config();

    MX_TIM2_Init();
    MX_TIM3_Init();

    HAL_TIM_IC_Start_IT(&htim2, TIM_CHANNEL_1);
    HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_1);
    HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_2);
    HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_3);
    HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_4);

    while (1)
    {
        read_rc_inputs();
        flight_control_update();
        write_motor_outputs();
        HAL_Delay(2); // ~500 Hz loop
    }
}
