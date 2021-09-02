function output = tables(in1 , in2 , in3 , in4 , in5)

% ----------------------------------------------------------------------------------------------
% Thermodynamic Properties for Water/Steam according to the IAPWS IF-97.
% Written by Julien Bassil and Georges Akiki, PhD (Notre Dame University, March 2019).
% Based on original works by Magnus Holmgren, Francois Brissette, and Philippe Daigle.
% ----------------------------------------------------------------------------------------------



% ----------------------------------------------------------------------------------------------
% UNITS OF INPUTS
% Pressure inputs and outputs are in bars
% Temperature inputs and outputs are in Degrees Celsius
% Specific enthalpy, specific entropy, and specific internal energy are in kJ / kg
% Specific volumes are in m^3 / kg
% Specific heat capacity (isobaric and isochoric) is in kJ / kg.K
% ----------------------------------------------------------------------------------------------



% ----------------------------------------------------------------------------------------------
% AVAILABLE FUNCTIONS
% Temperature	
% ( 'TSat' , 'P' )          Saturation temperature
% ( 'T' , 'P' , 'h' )       Temperature as a function of pressure and enthalpy
% ( 'T' , 'P' , 's' )       Temperature as a function of pressure and entropy
% ( 'T' , 'h' , 's' )       Temperature as a function of enthalpy and entropy
% ( 'T' , 'v' , 'P' )       Temperature as a function of specific volume and pressure
% ( 'T' , 'u' , 'P' )       Temperature as a function of internal energy and pressure
% 
% 
% Pressure	
% ( 'PSat' , 'T' )          Saturation pressure
% ( 'P' , 'h' , 's' )       Pressure as a function of enthalpy and entropy
% ( 'P' , 'v' , 'T' )       Pressure as a function of specific volume and enthalpy
% 
% 
% Enthalpy	
% ( 'hV' , 'P' )          Saturated vapour enthalpy as function of pressure
% ( 'hL' , 'P' )          Saturated liquid enthalpy as function of pressure
% ( 'hV' , 'T' )          Saturated vapour enthalpy as function of temperature
% ( 'hL' , 'T' )          Saturated liquid enthalpy as function of temperature
% ( 'h' , 'P' , 'T' )     Enthalpy as function of pressure and temperature
% ( 'h' , 'P' , 's' )     Enthalpy as function of pressure and entropy
% ( 'h' , 'P' , 'x' )     Enthalpy as function of pressure and quality
% ( 'h' , 'T' , 'x' )     Enthalpy as function of temperature and quality
% ( 'h' , 'v' , 'T' )     Enthalpy as function of specific volume and temperature
% ( 'h' , 'v' , 'P' )     Enthalpy as function of specific volume and pressure
% ( 'h' , 'u' , 'P' )     Enthalpy as function of internal energy and pressure
% ( 'h' , 'u' , 'T' )     Enthalpy as function of internal energy and temperature
% 
% 
% Specific volume	
% ( 'vV' , 'P' )          Saturated vapour volume as function of pressure
% ( 'vL' , 'P' )          Saturated liquid volume as function of pressure
% ( 'vV' , 'T' )          Saturated vapour volume as function of temperature
% ( 'vL' , 'T' )          Saturated liquid volume as function of temperature
% ( 'v' , 'P' , 'T' )     Volume as function of pressure and temperature
% ( 'v' , 'P' , 'h' )	  Specific volume as a function of pressure and enthalpy
% ( 'v' , 'P' , 's' )	  Specific volume as a function of pressure and entropy.
% ( 'v' , 'u' , 'P' )     Volume as function of internal energy and pressure
% ( 'v' , 'u' , 'T' )     Volume as function of internal energy and temperature
% 
%
% Specific entropy 	
% ( 'sV' , 'P' )          Saturated vapour entropy as function of pressure
% ( 'sL' , 'P' )          Saturated liquid entropy as function of pressure
% ( 'sV' , 'T' )          Saturated vapour entropy as function of temperature
% ( 'sL' , 'T' )          Saturated liquid entropy as function of temperature
% ( 's' , 'P' , 'T' )     Entropy as function of pressure and temperature
% ( 's' , 'P' , 'h' )	  Specific entropy as a function of pressure and enthalpy
% ( 's' , 'v' , 'T' )     Entropy as function of specific volume and temperature
% ( 's' , 'v' , 'P' )     Entropy as function of specific volume and pressure
% ( 's' , 'u' , 'P' )     Entropy as function of internal energy and pressure
% ( 's' , 'u' , 'T' )     Entropy as function of internal energy and temperature
% 
% 
% Specific internal energy
% ( 'uV' , 'P' )          Saturated vapour internal energy as function of pressure
% ( 'uL' , 'P' )          Saturated liquid internal energy as function of pressure
% ( 'uV' , 'T' )          Saturated vapour internal energy as function of temperature
% ( 'uL' , 'T' )          Saturated liquid internal energy as function of temperature
% ( 'u' , 'P' , 'T' )     Internal energy as function of pressure and temperature
% ( 'u' , 'P' , 'h' )	  Specific internal energy as a function of pressure and enthalpy
% ( 'u' , 'P' , 's' )	  Specific internal energy as a function of pressure and entropy.
% ( 'u' , 'v' , 'T' )     Internal energy as function of specific volume and temperature
% ( 'u' , 'v' , 'P' )     Internal energy as function of specific volume and pressure
% 
% 
% Specific isobaric heat capacity 	
% ( 'CpV' , 'P' )          Saturated vapour isobaric heat capacity as function of pressure
% ( 'CpL' , 'P' )          Saturated liquid isobaric heat capacity as function of pressure
% ( 'CpV' , 'T' )          Saturated vapour isobaric heat capacity as function of temperature
% ( 'CpL' , 'T' )          Saturated liquid isobaric heat capacity as function of temperature
% ( 'Cp' , 'P' , 'T' )     Isobaric heat capacity as function of pressure and temperature
% ( 'Cp' , 'P' , 'h' )     Isobaric heat capacity as a function of pressure and enthalpy
% ( 'Cp' , 'P' , 's' )     Isobaric heat capacity as a function of pressure and entropy.
%
% Specific isochoric heat capacity 	
% ( 'CvV' , 'P' )          Saturated vapour isochoric heat capacity as function of pressure
% ( 'CvL' , 'P' )          Saturated liquid isochoric heat capacity as function of pressure
% ( 'CvV' , 'T' )          Saturated vapour isochoric heat capacity as function of temperature
% ( 'CvL' , 'T' )          Saturated liquid isochoric heat capacity as function of temperature
% ( 'Cv' , 'P' , 'T' )     Isochoric heat capacity as function of pressure and temperature
% ( 'Cv' , 'P' , 'h' )     Isochoric heat capacity as a function of pressure and enthalpy
% ( 'Cv' , 'P' , 's' )     Isochoric heat capacity as a function of pressure and entropy.
% ----------------------------------------------------------------------------------------------



% ----------------------------------------------------------------------------------------------
% Examples of function in use // Inputs are NOT case sensitive
% Need 'T' from P = 100 bars and h = 3000 kJ/kg : T = tables( 'T' , 'P' , 'h' , 100 , 3000 )
% Need 'h' from u = 2500 kJ/kg and T = 90 C : h = tables( 'h' , 'u' , 'T' , 2500 , 90 )
% Need 's' from P = 50 bars and saturated vapor : s = tables( 'sV' , 'P' , 50 )
% 
% NOTE : 'L' after the property stands for saturated liquid // 'V' after the property stands 
% for saturated vapor
% ----------------------------------------------------------------------------------------------


% functions with two inputs from XSteam
XS_two_inputs = { 't_ph' , 't_ps' , 't_hs' , 'p_hs' , 'p_hrho' , 'h_pt' , ...
                  'h_ps' , 'h_px' , 'h_prho' , 'h_tx' , 'v_pt' , 'v_ph' , ...
                  'v_ps' , 's_pt' , 's_ph' , 'u_pt' , 'u_ph' , 'u_ps' , ...
                  'cp_pt' , 'cp_ph' , 'cp_ps' , 'cv_pt' , 'cv_ph' , 'cv_ps' , ...
                  'rho_pt' , 'rho_ph' , 'rho_ps' } ;

% functions with one input from XSteam
XS_one_input = { 'tsat_p' , 'psat_t' , 'hv_p' , 'hl_p' , 'hv_t' , 'hl_t' , ...
                 'vv_p' , 'vv_t' , 'vl_p' , 'vl_t' , 'sv_p' , 'sv_t' , ...
                 'sl_p' , 'sl_t' , 'uv_p' , 'uv_t' , 'ul_p' , 'ul_t' , ...
                 'cpv_p' , 'cpv_t' , 'cpl_p' , 'cpl_t' , 'cvv_p' , 'cvv_t' , ...
                 'cvl_p' , 'cvl_t' } ;

% checking which variable with which inputs the user needs
if isa( in3 , 'char' )
    in1 = lower(in1);
    in2 = lower(in2);
    in3 = lower(in3);
    needed = strcat(in1 , '_' , in2 , in3);
    for i = 1 : length(XS_two_inputs)
        if strcmp( needed , XS_two_inputs(i) )
            output = XSteam( needed , in4 , in5 );
            break
        end
    end

else
    in1 = lower(in1);
    in2 = lower(in2);
    needed = strcat( in1 , '_' , in2 );
    for j = 1 : length(XS_one_input)
        if strcmp( needed , XS_one_input(j) )
            output = XSteam( needed , in3);
            break
        end
    end
end

% checking WTP library for combinations that are not available in XSteam

% obtaining properties given 'v' and 'T'
if (strcmp( in2 , 'v' )) && (strcmp( in3 , 't' ))
    properties = WTP_vT( in4 , in5 );
    state_of_water = properties.state_of_water;
    
    switch state_of_water
        case 'subcooled liquid water'
            needed_property = strcat( in1 , 'f');
            switch needed_property
                case 'pf'
                    output = properties.pf;
                case 'tf'
                    output = properties.tf;
                case 'vf'
                    output = properties.vf;
                case 'uf'
                    output = properties.uf;
                case 'hf'
                    output = properties.hf;
                case 'sf'
                    output = properties.sf;
            end

         case 'superheated vapor water'
                needed_property = strcat( in1 , 'g');
                switch needed_property
                    case 'pg'
                        output = properties.pg;
                    case 'tg'
                        output = properties.tg;
                    case 'vg'
                        output = properties.vg;
                    case 'ug'
                        output = properties.ug;
                    case 'hg'
                        output = properties.hg;
                    case 'sg'
                        output = properties.sg;
                end

        case 'saturated water'
            needed_property = strcat( in1 , 't');
                switch needed_property
                    case 'pt'
                        output = properties.pf;
                    case 'tt'
                        output = properties.tf;
                    case 'vt'
                        output = properties.vt;
                    case 'ut'
                        output = properties.ut;
                    case 'ht'
                        output = properties.ht;
                    case 'st'
                        output = properties.st;
                    case 'x'
                        output = properties.x;
                end
    end

% obtaining properties given 'u' and 'P'
elseif (strcmp( in2 , 'u' )) && (strcmp( in3 , 'p' ))
    properties = WTP_uP( in4 , in5 );
    state_of_water = properties.state_of_water;

    switch state_of_water
        case 'subcooled liquid water'
            needed_property = strcat( in1 , 'f');
            switch needed_property
                case 'pf'
                    output = properties.pf;
                case 'tf'
                    output = properties.tf;
                case 'vf'
                    output = properties.vf;
                case 'uf'
                    output = properties.uf;
                case 'hf'
                    output = properties.hf;
                case 'sf'
                    output = properties.sf;
            end

         case 'superheated vapor water'
                needed_property = strcat( in1 , 'g');
                switch needed_property
                    case 'pg'
                        output = properties.pg;
                    case 'tg'
                        output = properties.tg;
                    case 'vg'
                        output = properties.vg;
                    case 'ug'
                        output = properties.ug;
                    case 'hg'
                        output = properties.hg;
                    case 'sg'
                        output = properties.sg;
                end

        case 'saturated water'
            needed_property = strcat( in1 , 't');
                switch needed_property
                    case 'pt'
                        output = properties.pf;
                    case 'tt'
                        output = properties.tf;
                    case 'vt'
                        output = properties.vt;
                    case 'ut'
                        output = properties.ut;
                    case 'ht'
                        output = properties.ht;
                    case 'st'
                        output = properties.st;
                    case 'x'
                        output = properties.x;
                end
    end


% obtaining properties given 'u' and 'T'
elseif (strcmp( in2 , 'u' )) && (strcmp( in3 , 't' ))
    properties = WTP_uT( in4 , in5 );
    state_of_water = properties.state_of_water;

    switch state_of_water
        case 'subcooled liquid water'
            needed_property = strcat( in1 , 'f');
            switch needed_property
                case 'pf'
                    output = properties.pf;
                case 'tf'
                    output = properties.tf;
                case 'vf'
                    output = properties.vf;
                case 'uf'
                    output = properties.uf;
                case 'hf'
                    output = properties.hf;
                case 'sf'
                    output = properties.sf;
            end

         case 'superheated vapor water'
                needed_property = strcat( in1 , 'g');
                switch needed_property
                    case 'pg'
                        output = properties.pg;
                    case 'tg'
                        output = properties.tg;
                    case 'vg'
                        output = properties.vg;
                    case 'ug'
                        output = properties.ug;
                    case 'hg'
                        output = properties.hg;
                    case 'sg'
                        output = properties.sg;
                end

        case 'saturated water'
            needed_property = strcat( in1 , 't');
                switch needed_property
                    case 'pt'
                        output = properties.pf;
                    case 'tt'
                        output = properties.tf;
                    case 'vt'
                        output = properties.vt;
                    case 'ut'
                        output = properties.ut;
                    case 'ht'
                        output = properties.ht;
                    case 'st'
                        output = properties.st;
                    case 'x'
                        output = properties.x;
                end
    end


% obtaining properties given 'v' and 'P'
elseif (strcmp( in2 , 'v' )) && (strcmp( in3 , 'p' ))
    properties = WTP_vP( in4 , in5 );
    state_of_water = properties.state_of_water;

    switch state_of_water
        case 'subcooled liquid water'
            needed_property = strcat( in1 , 'f');
            switch needed_property
                case 'pf'
                    output = properties.pf;
                case 'tf'
                    output = properties.tf;
                case 'vf'
                    output = properties.vf;
                case 'uf'
                    output = properties.uf;
                case 'hf'
                    output = properties.hf;
                case 'sf'
                    output = properties.sf;
            end

         case 'superheated vapor water'
                needed_property = strcat( in1 , 'g');
                switch needed_property
                    case 'pg'
                        output = properties.pg;
                    case 'tg'
                        output = properties.tg;
                    case 'vg'
                        output = properties.vg;
                    case 'ug'
                        output = properties.ug;
                    case 'hg'
                        output = properties.hg;
                    case 'sg'
                        output = properties.sg;
                end

        case 'saturated water'
            needed_property = strcat( in1 , 't');
                switch needed_property
                    case 'pt'
                        output = properties.pf;
                    case 'tt'
                        output = properties.tf;
                    case 'vt'
                        output = properties.vt;
                    case 'ut'
                        output = properties.ut;
                    case 'ht'
                        output = properties.ht;
                    case 'st'
                        output = properties.st;
                    case 'x'
                        output = properties.x;
                end
    end
end