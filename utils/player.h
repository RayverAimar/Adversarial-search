#ifndef __PLAYER_H__
#define __PLAYER_H__

struct Player
{
private:
    char avatar;
public:
    Player(char);
    ~Player();
    virtual void ask_for_movement();
    char get_icon();
};

Player::Player(char _avatar = ' ') : avatar(_avatar)
{
}

Player::~Player()
{
}

char Player::get_icon()
{
    return avatar;
}

#endif //__PLAYER_H__




#ifndef __HUMAN__
#define __HUMAN__

struct Human : public Player
{
private:
    /* data */
public:
    Human(char);
    ~Human();
    void ask_for_movement();
};

Human::Human(char avatar = 'O'): Player(avatar)
{
}

Human::~Human()
{
}

void Human::ask_for_movement(){
    /*
    Do Something
    */
}

#endif //__HUMAN__





#ifndef __COMPUTER__
#define __COMPUTER__

struct Computer : public Player
{
private:
    /* data */
public:
    Computer(char);
    ~Computer();
    void ask_for_movement();
};

Computer::Computer(char avatar = 'O'): Player(avatar)
{
}

Computer::~Computer()
{
}

void Computer::ask_for_movement(){
    /*
    Do another thing different from Human::ask_for_movement()
    */
}

#endif //__COMPUTER__

