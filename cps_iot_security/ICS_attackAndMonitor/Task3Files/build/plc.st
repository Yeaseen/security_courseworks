TYPE
  LOGLEVEL : (CRITICAL, WARNING, INFO, DEBUG) := INFO;
END_TYPE

FUNCTION_BLOCK LOGGER
  VAR_INPUT
    TRIG : BOOL;
    MSG : STRING;
    LEVEL : LOGLEVEL := INFO;
  END_VAR
  VAR
    TRIG0 : BOOL;
  END_VAR

  IF TRIG AND NOT TRIG0 THEN
  {{
   LogMessage(GetFbVar(LEVEL),(char*)GetFbVar(MSG, .body),GetFbVar(MSG, .len));
  }}
  END_IF;
  TRIG0:=TRIG;
END_FUNCTION_BLOCK


PROGRAM program0
  VAR_IN_OUT
    StartButton : BOOL;
    RollerEngine : BOOL;
    Nozzle : BOOL;
    BottleSensor : BOOL;
    WaterLevelSensor : BOOL;
    PlantState : INT;
  END_VAR

  (* Initialization Phase*)
      IF PlantState = 0 THEN
          RollerEngine := FALSE;
          Nozzle := FALSE;
          IF StartButton THEN
              PlantState := 1;         (* Move to Filling Phase*)
          END_IF;
      END_IF;

      (*Filling Phase*)
      IF PlantState = 1 THEN
          IF BottleSensor AND NOT WaterLevelSensor THEN
              Nozzle := TRUE;         (*Open the nozzle if bottle is under and not filled*)
          ELSE
              Nozzle := FALSE;        (* Close the nozzle otherwise*)
          END_IF;

          IF WaterLevelSensor THEN
              PlantState := 2;        (*Move to Moving Phase once bottle is filled*)
          END_IF;
      END_IF;

      (*Moving Phase*)
      IF PlantState = 2 THEN
          Nozzle := FALSE;            (* Ensure nozzle is closed*)
          RollerEngine := TRUE;        (* Start the roller engine to move the bottle*)

          IF NOT BottleSensor THEN
              PlantState := 1;         (*Move back to Filling Phase once bottle has moved away*)
          END_IF;
      END_IF;

    (* Stop the plant if StartButton is turned off*)
      IF NOT StartButton THEN
          PlantState := 0;
      END_IF;
END_PROGRAM


CONFIGURATION Config0

  RESOURCE Res0 ON PLC
    TASK task0(INTERVAL := T#20ms,PRIORITY := 0);
    PROGRAM instance0 WITH task0 : program0;
  END_RESOURCE
END_CONFIGURATION
