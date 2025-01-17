using UnityEngine;

//Clase para guardar las preferencias del usuario en cuanto a sonido
[System.Serializable]
public class SonidoPref
{
    public float sfxVolume;
    public float musicVolumen;

    public SonidoPref(float sfx, float volumen)
    {
        this.sfxVolume = sfx;
        this.musicVolumen = volumen;
    }
}
