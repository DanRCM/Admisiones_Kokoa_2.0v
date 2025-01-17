using System;
using UnityEngine;


public class AudioManager : MonoBehaviour
{
    public Sonido[] musicas,sfxSonidos;
    public AudioSource musicSource;
    private float sfxVolumen;

    public static AudioManager instance;

    private void Awake()
    {
        if (instance == null)
        {
            instance = this;
        }
    }



    //Funcion para tocar musica
    public void PlayMusic(string nombre)
    {
        //Busca en el array el objeto con el mismo nombre
        Sonido s = Array.Find(musicas, x=> x.nombre == nombre);

        //Si lo encuentra reproduce el sonido
        if (s != null) 
        { 
            musicSource.clip = s.clip;
            musicSource.Play();
        }
    }

    public void PlaySfx(string nombre)
    {
        //Lo mismo que antes
        Sonido s = Array.Find(sfxSonidos, x => x.nombre == nombre);

        if (s != null)
        {
            // En este caso creo temporalmente un objeto de audio
            AudioSource tempSource = gameObject.AddComponent<AudioSource>();

            //Donde reproduzco el sonido con un pitch aleatorio entre 0.9 y 1.1 para que no sea tan repetetivo.
            
            tempSource.clip = s.clip;
            tempSource.pitch = UnityEngine.Random.Range(0.9f, 1.1f);
            tempSource.volume = sfxVolumen;
            
            tempSource.Play();

            // Destruir el AudioSource temporal cuando el clip haya terminado
            Destroy(tempSource, s.clip.length);
        }
    }

    public void musicVolumen(float volumen)
    {
        musicSource.volume = volumen;
    }

    public void sfxSound(float volumen) 
    {
        sfxVolumen = volumen;
    }
}
