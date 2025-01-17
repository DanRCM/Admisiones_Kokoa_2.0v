using UnityEngine;


[System.Serializable]
public class PlayerData
{
    public int monedasUsables;
    public float puntajeAlto;
    public bool canDash;
    public int doblesSaltos;

    public PlayerData(int monedas, float puntaje,bool candash,int doubleJumps)
    {
        this.monedasUsables = monedas;
        this.puntajeAlto = puntaje;
        this.canDash = candash;
        this.doblesSaltos = doubleJumps;
    }   
}
