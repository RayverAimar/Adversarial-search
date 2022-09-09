#ifndef __TIC_TAC_TOE_H__
#define __TIC_TAC_TOE_H__

#include <iostream>

#include "./utils.h"

struct TicTacToe
{
private:
    TIC_TAC_TOE_BOARD board;
public:
    
    TicTacToe(unsigned int);
    ~TicTacToe();

    void draw();
    void insert_movement(char, int);

    TIC_TAC_TOE_BOARD get_status();
};

TicTacToe::TicTacToe(unsigned int n = 3)
{
    board = TIC_TAC_TOE_BOARD(n, TIC_TAC_TOE_ROW(n, ' '));
    
}

TicTacToe::~TicTacToe()
{
}

TIC_TAC_TOE_BOARD TicTacToe::get_status(){
    return board;
}

void TicTacToe::draw(){
    for(unsigned int i = 0; i < board.size(); i++)
    {
        for(unsigned int j = 0; j < board[i].size(); j++)
        {
            std::cout << board[i][j] << "-";
        }
        std::cout<<"\n";
    }
}

void insert_movement(char avatar, int pos){
    //Given a position and an avatar insert movement on board
}


#endif //__TIC_TAC_TOE_H__