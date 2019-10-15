#include <iostream>
#include <time.h>
#include <windows.h>
#include "keyboard.h"
#include "class.h"
#include "score_file.h"
using namespace std;

void end_game(int score)
{
    // paint background
    // update screen
    string player_name="cyy";
    string score_file_name="C:/Users/cyy/Desktop/SnakeGame/high_score_list.dat";
    int high_score_list[2][10]=read_score_file(score_file_name)
}

void Game()
{
    double max_fps = 3.0;
    // board=Board();
    // snake=[];

    int score = 0;
    int last_press = 1;
    int current_frame = 0;
    // board.generate_food();
    double start_time = clock();

    // paint background color
    // update screen

    bool game_is_on = true;
    int press, last_press = 1;
    while (game_is_on)
    {
        if ((clock() - start_time) * max_fps > current_frame)
        {
            current_frame++;
            int press = reveive_keyboard();
            if (press == 0)
                press = last_press;
            else
                last_press = press;
            int status = board.snake_move();
            if (status == 1)
            {
                score += 100;
                board.generate_food();
            }
            else if (status == 2)
            {
                end_game(score);
                game_is_on = false;
            }
            // print background
            // draw snake
            // draw food
            // update screen
        }
    }
}

void Main()
{
    clock_t start_time;
    // TODO here is a title

    // TODO here is a menu

    // 无限执行刷新
    while (true)
    {
        current_frame++;
        // get keyboard event
        Game();
        // use event to update menu

        // handle quit event

        // draw
    }
}
int main()
{
    Main();
}