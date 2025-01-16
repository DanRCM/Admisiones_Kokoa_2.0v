using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Audio;
using System.Collections.Generic;
using TMPro;

public class MenuOpciones : MonoBehaviour
{

    //Estas son las funcionalidades del menu de opciones(esto es lo unico que copie al 100% y no se como funciona del todo.
    [Header("UI Elements")]
    public Toggle fullscreenToggle;
    public TMP_Dropdown resolutionDropdown;


    private Resolution[] resolutions;

    void Start()
    {
        // Inicializar resoluciones
        InitializeResolutions();

        // Cargar configuraciones guardadas
        LoadSettings();
    }

    void InitializeResolutions()
    {
        resolutions = Screen.resolutions;
        resolutionDropdown.ClearOptions();

        List<string> options = new List<string>();
        int currentResolutionIndex = 0;

        for (int i = 0; i < resolutions.Length; i++)
        {
            string option = resolutions[i].width + " x " + resolutions[i].height;
            options.Add(option);

            if (resolutions[i].width == Screen.currentResolution.width &&
                resolutions[i].height == Screen.currentResolution.height)
            {
                currentResolutionIndex = i;
            }
        }

        resolutionDropdown.AddOptions(options);
        resolutionDropdown.value = currentResolutionIndex;
        resolutionDropdown.RefreshShownValue();
    }

    public void SetFullScreen(bool isFullScreen)
    {
        Screen.fullScreen = isFullScreen;
        PlayerPrefs.SetInt("fullscreen", isFullScreen ? 1 : 0);
       
    }

    public void SetResolution(int resolutionIndex)
    {
        Resolution resolution = resolutions[resolutionIndex];
        Screen.SetResolution(resolution.width, resolution.height, Screen.fullScreen);
        PlayerPrefs.SetInt("resolution", resolutionIndex);
      
    }

   

    public void LoadSettings()
    {
        // Pantalla completa
        if (PlayerPrefs.HasKey("fullscreen"))
        {
            bool isFullScreen = PlayerPrefs.GetInt("fullscreen") == 1;
            fullscreenToggle.isOn = isFullScreen;
            Screen.fullScreen = isFullScreen;
        }


        // Resolución
        if (PlayerPrefs.HasKey("resolution"))
        {
            int resolutionIndex = PlayerPrefs.GetInt("resolution");
            if (resolutionIndex < resolutions.Length)
            {
                resolutionDropdown.value = resolutionIndex;
                Resolution resolution = resolutions[resolutionIndex];
                Screen.SetResolution(resolution.width, resolution.height, Screen.fullScreen);
            }
        }

    }
}
