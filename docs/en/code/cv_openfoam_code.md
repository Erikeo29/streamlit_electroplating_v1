# Configuration: CV OpenFOAM

Excerpts from OpenFOAM configuration dictionaries.

## 1. Transport Properties (`constant/transportProperties`)
```cpp
// Ferrocyanide Diffusion
D           7.0e-9;
```

## 2. Butler-Volmer Condition (`0/c_R`)
Implementation often relies on `codedFixedValue` for flux:
```cpp
patchName
{
    type            codedFixedValue;
    value           uniform 1.0;
    name            butlerVolmer;
    
    code
    #{
        // Flux calculation based on E(t)
        // J = k0 * (cR * exp(a*f*eta) - cO * exp(-ac*f*eta))
    #};
}
```

## 3. Time Scheme (`system/controlDict`)
```cpp
application     electroChemFoam;
startFrom       startTime;
startTime       0;
stopAt          endTime;
endTime         100;
deltaT          0.01;
writeControl    runTime;
writeInterval   1;
```